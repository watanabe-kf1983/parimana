import { uniqWith, isEqual } from "lodash";
import { useEffect, useState } from "react";
import useSWR from "swr";
import { Box } from "@mui/material";

import {
  Category,
  RaceInfo,
  RaceSelectorProps,
} from "../types";
import { CategorySelector } from "./CategorySelector";
import { DateSelector } from "./DateSelector";
import { RaceOnDaySelector } from "./RaceOnDaySelector";
import { CourseSelector } from "./CourseSelector";
import * as api from "../api";


const fetchCategories = async (_params: any): Promise<Category[]> => {
  return await api.getCategories();
};

const fetchSchedule = async (params: {
  categoryId?: string;
}): Promise<RaceInfo[]> => {
  if (params.categoryId) {
    return await api.getCalendar(params.categoryId);
  } else {
    return [];
  }
};

const fetchRaceInfo = async (raceId: string): Promise<RaceInfo | undefined> => {
  if (raceId) {
    return await api.getRaceInfo(raceId);
  } else {
    return undefined;
  }
};

const appendCategory = (categories: Category[] | undefined, additional: RaceInfo | undefined) => {
  const arrayA = categories || []
  const arrayB = additional ? [additional.fixture.course.category] : []
  return uniqWith([...arrayA, ...arrayB], isEqual)
}

const appendSchedule = (schedule: RaceInfo[] | undefined, additional: RaceInfo | undefined) => {
  const arrayA = schedule || []
  const arrayB = additional ? [additional] : []
  return uniqWith([...arrayA, ...arrayB], isEqual)
}

export function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState<string>(props.raceId);
  const [categoryId, setCategoryId] = useState<string | undefined>();
  const [date, setDate] = useState<string | undefined>();
  const [courseId, setCourseId] = useState<string | undefined>();
  const [raceInfo, setRaceInfo] = useState<RaceInfo | undefined>();

  useEffect(() => {
    const getRI = async () => {
      const ri = await fetchRaceInfo(props.raceId);
      if (ri) {
        setRaceInfo(ri);
        setCategoryId(ri.fixture.course.category.id);
        setDate(ri.fixture.date);
        setCourseId(ri.fixture.course.id);
      }
    };
    getRI();
  }, [props.raceId]);

  const fetchedCategories = useSWR<Category[]>(
    "x",
    fetchCategories
  ).data;

  const fetchedSchedule = useSWR<RaceInfo[] | undefined>(
    { categoryId },
    fetchSchedule
  ).data;

  const categories = appendCategory(fetchedCategories, raceInfo)
  const schedule = appendSchedule(fetchedSchedule, raceInfo)

  const categoryItems = categories.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

  const dateItems =
    uniqWith(
      schedule
        .filter((r) => categoryId === r.fixture.course.category.id)
        .map((r) => r.fixture.date),
      isEqual
    ).sort();

  const courseItems =
    uniqWith(
      schedule
        .filter((r) => categoryId === r.fixture.course.category.id)
        .filter((r) => date === r.fixture.date)
        .map((r) => r.fixture.course),
      isEqual
    ).sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

  const raceItems =
    schedule
      .filter((r) => categoryId === r.fixture.course.category.id)
      .filter((r) => date === r.fixture.date)
      .filter((r) => courseId === r.fixture.course.id)
      .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));


  const onChangeCategoryId = (cid: string) => {
    setCategoryId(cid);
    setDate(undefined);
    setCourseId(undefined);
    setRaceId("");
  };
  const onChangeDate = (d: string) => {
    setCourseId(undefined);
    setRaceId("");
    setDate(d);
  };
  const onChangeCourseId = (cid: string) => {
    setCourseId(cid);
    setRaceId("");
  };

  return (
    <>
      <Box sx={{
        m: 2,
        flexDirection: 'row'
      }} >
        <CategorySelector
          value={categoryId}
          items={categoryItems}
          onChange={onChangeCategoryId}
        />
        <DateSelector
          value={date}
          items={dateItems}
          onChange={onChangeDate}
        />
        <CourseSelector
          value={courseId}
          items={courseItems}
          onChange={onChangeCourseId}
        />
        <RaceOnDaySelector
          value={raceId}
          items={raceItems}
          onChange={(rid) => {
            setRaceId(rid);
            props.onSetRaceId(rid);
          }}
        />
      </Box>
    </>
  );
}

import { useEffect, useState } from "react";
import { TextField, Typography } from "@mui/material";
import useSWR from "swr";

import { Calendar, Category, RaceInfo, RaceSelectorProps } from "../types";
import { CategorySelector } from "./CategorySelector";
import { DateSelector } from "./DateSelector";
import { RaceOnDaySelector } from "./RaceOnDaySelector";
import { CourseSelector } from "./CourseSelector";
import * as api from "../api";

const fetchCategories = async (_params: any): Promise<Category[]> => {
  return await api.getCategories();
};

const fetchCalendar = async (params: {
  categoryId?: string;
  additionalRace?: RaceInfo;
}): Promise<Calendar | undefined> => {
  if (params.categoryId) {
    return await api.getCalendar(params.categoryId);
  } else {
    return undefined;
  }
};

const fetchRaceInfo = async (raceId: string): Promise<RaceInfo | undefined> => {
  if (raceId) {
    return await api.getRaceInfo(raceId);
  } else {
    return undefined;
  }
};

export function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState<string>(props.raceId);
  const [categoryId, setCategoryId] = useState<string | undefined>();
  const [date, setDate] = useState<string | undefined>();
  const [courseId, setCourseId] = useState<string | undefined>();
  const [raceInfo, setRaceInfo] = useState<RaceInfo | undefined>();

  useEffect(() => {
    const getRI = async () => {
      const ri = await fetchRaceInfo(props.raceId);
      setRaceInfo(ri);
      setCategoryId(ri?.fixture.category.id);
      setDate(ri?.fixture.date);
      setCourseId(ri?.fixture.course.id);
    };
    getRI();
  }, [props.raceId]);

  const categoryItems = useSWR<Category[] | undefined>(
    "x",
    fetchCategories
  ).data;
  const calendar = useSWR<Calendar | undefined>(
    { categoryId, additionalRace: raceInfo },
    fetchCalendar
  ).data;

  const dateItems = calendar ? Object.keys(calendar) : undefined;
  const courseItems =
    calendar && date ? calendar[date].map((o) => o.course) : undefined;
  const raceItems =
    calendar && date && courseId
      ? calendar[date].find((o) => o.course.id === courseId)?.races
      : undefined;

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
      <CategorySelector
        value={categoryId}
        items={categoryItems}
        onChange={onChangeCategoryId}
      />
      <DateSelector value={date} items={dateItems} onChange={onChangeDate} />
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
      {/* <TextField
        sx={{ width: "30ch" }}
        value={raceId}
        onChange={(e) => setRaceId(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            props.onSetRaceId(raceId);
          }
        }}
        onBlur={() => props.onSetRaceId(raceId)}
      /> */}
    </>
  );
}

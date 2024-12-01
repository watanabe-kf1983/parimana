import { useEffect, useState } from "react";
import { TextField, Typography } from "@mui/material";
import useSWR from "swr";

import {
  Calendar,
  Category,
  Course,
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

const fetchCalendar = async (params: {
  categoryId?: string;
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
      if (ri) {
        setRaceInfo(ri);
        setCategoryId(ri.fixture.category.id);
        setDate(ri.fixture.date);
        setCourseId(ri.fixture.course.id);
      }
    };
    getRI();
  }, [props.raceId]);

  const categoryItems = useSWR<Category[] | undefined>(
    "x",
    fetchCategories
  ).data;

  const calendar = useSWR<Calendar | undefined>(
    { categoryId },
    fetchCalendar
  ).data;

  const collectCategoryItems = () => {
    const items: Category[] = [];
    if (categoryItems) {
      categoryItems.forEach((c) => items.push(c));
    }
    if (raceInfo) {
      if (!items.find((c) => c.id === raceInfo.fixture.category.id)) {
        items.push(raceInfo);
      }
    }
    return items.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  };

  const collectDateItems = () => {
    const set = new Set<string>();
    if (calendar) {
      Object.keys(calendar).forEach((date) => set.add(date));
    }
    if (raceInfo && raceInfo.fixture.category.id === categoryId) {
      set.add(raceInfo.fixture.date);
    }
    return Array.from(set).sort();
  };

  const collectCourseItems = () => {
    const items: Course[] = [];
    if (calendar && date) {
      calendar[date]?.forEach((schedule) => items.push(schedule.course));
    }
    if (
      raceInfo &&
      raceInfo.fixture.category.id === categoryId &&
      raceInfo.fixture.date === date
    ) {
      if (!items.find((c) => c.id === raceInfo.fixture.course.id)) {
        items.push(raceInfo.fixture.course);
      }
    }
    return items.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  };

  const collectRaceItems = () => {
    const items: RaceInfo[] = [];
    if (calendar && date && courseId) {
      calendar[date]
        ?.find((o) => o.course.id === courseId)
        ?.races.forEach((r) => items.push(r));
    }
    if (
      raceInfo &&
      raceInfo.fixture.category.id === categoryId &&
      raceInfo.fixture.date === date &&
      raceInfo.fixture.course.id == courseId
    ) {
      if (!items.find((r) => r.id === raceInfo.id)) {
        items.push(raceInfo);
      }
    }
    return items.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  };

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
        items={collectCategoryItems()}
        onChange={onChangeCategoryId}
      />
      <DateSelector
        value={date}
        items={collectDateItems()}
        onChange={onChangeDate}
      />
      <CourseSelector
        value={courseId}
        items={collectCourseItems()}
        onChange={onChangeCourseId}
      />
      <RaceOnDaySelector
        value={raceId}
        items={collectRaceItems()}
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

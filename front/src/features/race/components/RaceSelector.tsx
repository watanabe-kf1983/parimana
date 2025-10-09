import { useEffect, useState } from "react";
import { uniqWith, isEqual } from "lodash";
import { Box } from "@mui/material";

import { RaceInfo } from "../types";
import * as api from "../api";
import { DateSelector } from "./DateSelector";
import { CategorySelector } from "./CategorySelector";
import { RaceOnDaySelector } from "./RaceOnDaySelector";
import { CourseSelector } from "./CourseSelector";
import { UriForm } from "./UriForm";

const fetchRaceInfo = async (raceId: string): Promise<RaceInfo | undefined> => {
  if (raceId) {
    try {
      return await api.getRaceInfo(raceId);
    } catch (e) {
      if (e instanceof api.NotFoundError) {
        throw e;
      }
    }
  }
  return undefined;
}

const merge = (a: RaceInfo[] | RaceInfo | undefined, b: RaceInfo[] | RaceInfo | undefined) => {
  const arrayA = Array.isArray(a) ? a : (a ? [a] : [])
  const arrayB = Array.isArray(b) ? b : (b ? [b] : [])
  return uniqWith([...arrayA, ...arrayB], isEqual)
}

type Props = {
  initialRaceId?: string;
  showControl: boolean;
  onClearRaceId: () => void;
  onSetRaceId: (input: string) => void;
};

export function RaceSelector(props: Props) {
  const [raceId, setRaceId] = useState<string | undefined>(props.initialRaceId);
  const [raceInfo, setRaceInfo] = useState<RaceInfo | undefined>();
  const [categoryId, setCategoryId] = useState<string | undefined>();
  const [date, setDate] = useState<string | undefined>();
  const [courseId, setCourseId] = useState<string | undefined>();
  const [recentRaces, setRecentRaces] = useState<RaceInfo[]>([]);

  useEffect(() => {
    const getRecentRaces = async () => {
      const races = await api.getRaces(!props.showControl);
      setRecentRaces(races)
    }
    getRecentRaces();

    const interval = setInterval(() => {
      getRecentRaces();
    }, 60000);

    return () => clearInterval(interval);
  }, [props.showControl]);

  useEffect(() => {
    const getRaceInfo = async () => {
      if (!props.initialRaceId) {
        return
      }
      for (let i: number = 0; i < 20; i++) {
        try {
          const ri = await fetchRaceInfo(props.initialRaceId);
          onFetchRaceInfo(ri);
          return;

        } catch (e) {

          onFetchRaceInfo(undefined);
          if (!(props.showControl && e instanceof api.NotFoundError)) {
            return;
          }
          if (i === 0) {
            await api.postRaceInfo(props.initialRaceId);
          }
          await new Promise(resolve => setTimeout(resolve, 2000));
          continue;
        }
      }
    }
    getRaceInfo();
  }, [props.initialRaceId, props.showControl]);

  const candidates = merge(recentRaces, raceInfo);

  const categoryItems = uniqWith(
    candidates.map((r) => r.fixture.course.category),
    isEqual
  ).sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

  const dateItems =
    uniqWith(
      candidates
        .filter((r) => categoryId === r.fixture.course.category.id)
        .map((r) => r.fixture.date),
      isEqual
    ).sort();

  const courseItems =
    uniqWith(
      candidates
        .filter((r) => categoryId === r.fixture.course.category.id)
        .filter((r) => date === r.fixture.date)
        .map((r) => r.fixture.course),
      isEqual
    ).sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

  const raceItems =
    candidates
      .filter((r) => categoryId === r.fixture.course.category.id)
      .filter((r) => date === r.fixture.date)
      .filter((r) => courseId === r.fixture.course.id)
      .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));


  const onFetchRaceInfo = (ri: RaceInfo | undefined) => {
    if (ri) {
      setRaceInfo(ri);
      setCategoryId(ri.fixture.course.category.id);
      setDate(ri.fixture.date);
      setCourseId(ri.fixture.course.id);
    } else {
      setRaceInfo(undefined);
      setCategoryId(undefined);
      setDate(undefined);
      setCourseId(undefined);
    }
  };
  const onChangeCategoryId = (cid: string) => {
    setCategoryId(cid);
    setDate(undefined);
    setCourseId(undefined);
    setRaceId(undefined);
    props.onClearRaceId()
  };
  const onChangeDate = (d: string) => {
    setDate(d);
    setCourseId(undefined);
    setRaceId(undefined);
    props.onClearRaceId()
  };
  const onChangeCourseId = (cid: string) => {
    setCourseId(cid);
    setRaceId(undefined);
    props.onClearRaceId()
  };
  const onSetRaceId = (rid: string) => {
    setRaceId(rid);
    props.onSetRaceId(rid);
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
          onChange={onSetRaceId}
        />
        {props.showControl
          ? <UriForm onRaceIdFound={onSetRaceId} />
          : null
        }
      </Box>
    </>
  );
}

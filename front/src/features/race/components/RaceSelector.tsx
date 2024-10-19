import { useState } from "react";
import { TextField } from "@mui/material";
import { RaceSelectorProps } from "../types";
import { CategorySelector } from "./CategorySelector";
import { DateSelector } from "./DateSelector";

const getCategories = () => [
  { id: "1", name: "boat" },
  { id: "2", name: "horse" },
];

const getDates = (catId: string) => [`2024-0${catId}-01`, `2024-0${catId}-02`];

const getCourses = (catId: string, date: string) =>
  catId === "1"
    ? [
        { id: "101", name: "Kiryu" },
        { id: "102", name: "Toda" },
      ]
    : [
        { id: "201", name: "Fuchu" },
        { id: "202", name: "Nakayama" },
      ];

export function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState(props.raceId);
  const [catId, setCatId] = useState<string>("");
  const [date, setDate] = useState<string>("");
  const selectRace = () => {
    props.onSetRaceId(raceId);
  };
  const selectCategory = (c: string) => {
    setCatId(c);
    setDate(getDates(c)[0]);
  };
  const selectDate = (d: string) => {
    setDate(d);
  };

  return (
    <>
      <CategorySelector
        value={catId}
        items={getCategories()}
        onSetCategoryId={selectCategory}
      />
      <DateSelector
        value={date}
        items={getDates(catId)}
        onSetDate={selectDate}
      />
      <TextField
        sx={{ width: "30ch" }}
        value={raceId}
        onChange={(e) => setRaceId(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            selectRace();
          }
        }}
        onBlur={selectRace}
      />
    </>
  );
}

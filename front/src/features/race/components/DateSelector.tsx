// import { useState } from "react";
import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { DateSelectorProps } from "../types";

export function DateSelector(props: DateSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onSetDate(event.target.value);
  };

  return props.items.length ? (
    <>
      <Select
        value={props.value}
        onChange={handleChange}
      >
        {props.items.map((item) => (
          <MenuItem value={item}>{item}</MenuItem>
        ))}
      </Select>
    </>
  ) : null;
}

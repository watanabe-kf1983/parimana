// import { useState } from "react";
import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CategorySelectorProps } from "../types";

export function CategorySelector(props: CategorySelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onSetCategoryId(event.target.value);
  };

  return props.items.length ? (
    <>
      <Select
        value={props.value}
        onChange={handleChange}
      >
        {props.items.map((item) => (
          <MenuItem value={item.id}>{item.name}</MenuItem>
        ))}
      </Select>
    </>
  ) : null;
}

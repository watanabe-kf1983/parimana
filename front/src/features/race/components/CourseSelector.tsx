import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CourseSelectorProps } from "../types";

export function CourseSelector(props: CourseSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <Select
        value={props.value}
        onChange={handleChange}
      >
        {props.items?.map((item) => (
          <MenuItem value={item.id}>{item.name}</MenuItem>
        ))}
      </Select>
    </>
  );
}

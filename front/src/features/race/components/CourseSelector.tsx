import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CourseSelectorProps } from "../types";

export function CourseSelector(props: CourseSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 100
      }} >
        <InputLabel id="course-selector-label">開催場</InputLabel>
        <Select value={props.value} key={props.value} onChange={handleChange}
          label="開催場" labelId="course-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item.id}>{item.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

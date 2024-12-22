import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CourseSelectorProps } from "../types";

export function CourseSelector(props: CourseSelectorProps) {

  // To avoid "Consider providing a value that matches one of the available options or ''""
  const value = props.items?.find((item) => item.id == props.value) ? props.value : ""

  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 100
      }} >
        <InputLabel id="course-selector-label">開催場</InputLabel>
        <Select value={value} onChange={handleChange}
          label="開催場" labelId="course-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item.id} key={"cr_item_" + item.id}>{item.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

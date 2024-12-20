import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { DateSelectorProps } from "../types";

export function DateSelector(props: DateSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 130
      }} >
        <InputLabel id="date-selector-label">開催日</InputLabel>
        <Select value={props.value} key={props.value} onChange={handleChange}
          label="開催日" labelId="date-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item}>{item}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

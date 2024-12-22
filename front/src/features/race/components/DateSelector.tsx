import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { DateSelectorProps } from "../types";

export function DateSelector(props: DateSelectorProps) {

  // To avoid "Consider providing a value that matches one of the available options or ''""
  const value = props.items?.find((item) => item == props.value) ? props.value : ""

  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 130
      }} >
        <InputLabel id="date-selector-label">開催日</InputLabel>
        <Select value={value} onChange={handleChange}
          label="開催日" labelId="date-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item} key={"dt_item_" + item}>{item}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

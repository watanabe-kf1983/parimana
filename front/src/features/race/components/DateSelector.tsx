import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { DateSelectorProps } from "../types";

export function DateSelector(props: DateSelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <Select value={props.value} key={props.value} onChange={handleChange}>
        {props.items?.map((item) => (
          <MenuItem value={item}>{item}</MenuItem>
        ))}
      </Select>
    </>
  );
}

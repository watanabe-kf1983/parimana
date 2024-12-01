import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { RaceOnDaySelectorProps } from "../types";

export function RaceOnDaySelector(props: RaceOnDaySelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <Select value={props.value} key={props.value} onChange={handleChange}>
        {props.items?.map((race) => (
          <MenuItem value={race.id}>{race.name}</MenuItem>
        ))}
      </Select>
    </>
  );
}

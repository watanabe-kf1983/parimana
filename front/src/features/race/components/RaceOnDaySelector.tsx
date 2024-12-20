import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { RaceOnDaySelectorProps } from "../types";

export function RaceOnDaySelector(props: RaceOnDaySelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 80
      }}>
        <InputLabel id="race-selector-label">レース</InputLabel>
        <Select value={props.value} key={props.value} onChange={handleChange}
          label="レース" labelId="race-selector-label">
          {props.items?.map((race) => (
            <MenuItem value={race.id}>{race.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

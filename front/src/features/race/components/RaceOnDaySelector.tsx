import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { RaceInfo } from "../types";

type Props = {
  value?: string;
  items?: RaceInfo[];
  onChange: (input: string) => void;
};

export function RaceOnDaySelector(props: Props) {

  // To avoid "Consider providing a value that matches one of the available options or ''""
  const value = props.items?.find((race) => race.id == props.value) ? props.value : ""

  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 80
      }}>
        <InputLabel id="race-selector-label">レース</InputLabel>
        <Select value={value} onChange={handleChange}
          label="レース" labelId="race-selector-label">
          {props.items?.map((race) => (
            <MenuItem value={race.id} key={"rc_item_" + race.id}>{race.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

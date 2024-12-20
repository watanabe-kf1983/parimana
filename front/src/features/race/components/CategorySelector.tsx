import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CategorySelectorProps } from "../types";

export function CategorySelector(props: CategorySelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 80
      }} >
        <InputLabel id="category-selector-label">競技</InputLabel>
        <Select value={props.value} key={props.value} onChange={handleChange}
          label="競技" labelId="category-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item.id}>{item.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

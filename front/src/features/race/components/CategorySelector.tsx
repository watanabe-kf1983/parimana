import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CategorySelectorProps } from "../types";

export function CategorySelector(props: CategorySelectorProps) {

  // To avoid "Consider providing a value that matches one of the available options or ''""
  const value = props.items?.find((item) => item.id == props.value) ? props.value : ""

  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <FormControl size="small" sx={{
        minWidth: 80
      }} >
        <InputLabel id="category-selector-label">競技</InputLabel>
        <Select value={value} onChange={handleChange}
          label="競技" labelId="category-selector-label">
          {props.items?.map((item) => (
            <MenuItem value={item.id} key={"ct_item_" + item.id}>{item.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </>
  );
}

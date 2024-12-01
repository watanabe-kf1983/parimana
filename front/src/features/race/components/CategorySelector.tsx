import { MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { CategorySelectorProps } from "../types";

export function CategorySelector(props: CategorySelectorProps) {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <Select value={props.value} key={props.value} onChange={handleChange}>
        {props.items?.map((item) => (
          <MenuItem value={item.id}>{item.name}</MenuItem>
        ))}
      </Select>
    </>
  );
}

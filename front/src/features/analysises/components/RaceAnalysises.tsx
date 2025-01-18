import { Tab, Tabs } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { RaceProps } from '../types';
import { Analysis } from './Analysis';
import { useState } from 'react';

export function RaceAnalysises(props: RaceProps) {

  const [value, setValue] = useState(0);

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  const theme = useTheme();
  return (
    <>
      <Tabs
        value={value} onChange={handleChange} sx={{
          position: 'sticky',
          top: 96,
          zIndex: theme.zIndex.appBar,
          backgroundColor: theme.palette.background.default
        }}>
        <Tab label="さっくりモデル" />
        <Tab label="ふんわりモデル" />
      </Tabs>
      <div hidden={value !== 0}>
        {value === 0 ?
          <Analysis raceId={props.raceId} modelName="no_cor" />
          : null}
      </div>
      <div hidden={value !== 1}>
        {value === 1 ?
          <Analysis raceId={props.raceId} modelName="ppf_mtx" />
          : null}
      </div>
    </>
  )
}

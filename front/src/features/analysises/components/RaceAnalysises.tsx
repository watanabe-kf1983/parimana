import { useState } from 'react';
import { Tab, Tabs } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Analysis } from './Analysis';
import { getModelLabel, MODELS } from '../../models/types';


type Props = { raceId: string };

export function RaceAnalysises(props: Props) {

  const [tabIndex, setTabIndex] = useState(0);
  const modelList = MODELS;
  const modelName = modelList[tabIndex];

  const handleTabChange = (_event: React.SyntheticEvent, newIndex: number) => {
    setTabIndex(newIndex);
  };
  const theme = useTheme();

  return (
    <>
      <Tabs
        value={tabIndex} onChange={handleTabChange} sx={{
          position: 'sticky',
          top: 96,
          zIndex: theme.zIndex.appBar,
          backgroundColor: theme.palette.background.default
        }}>
        {modelList.map(name => (
          <Tab key={name} label={getModelLabel(name)} />
        ))}
      </Tabs>
      <Analysis key={`${props.raceId}-${modelName}`} raceId={props.raceId} modelName={modelName} />
    </>
  )
}

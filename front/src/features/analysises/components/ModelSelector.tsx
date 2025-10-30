import { useEffect, useState } from 'react';
import { Tab, Tabs, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';

import { getModelLabel } from '../../models/types';
import { getLatestModelList } from '../api';
import { ModelKey } from '../types';


type Props = {
  raceId: string,
  onModelSelect: (input: ModelKey | undefined) => void
  onSetFetching: (input: boolean) => void,
};

export function ModelSelector(props: Props) {

  const [modelName, setModelName] = useState<string>("model_unexist");
  const [modelList, setModelList] = useState<string[] | false>(() => false);
  const theme = useTheme();

  useEffect(() => {
    const getList = async () => {
      props.onSetFetching(true);
      const list = await getLatestModelList(props.raceId);
      onModelListSet(list);
      props.onSetFetching(false);
    }
    getList();
  }, [props.raceId])

  const onModelNameSet = (name: string) => {
    setModelName(name);
    props.onModelSelect({ raceId: props.raceId, modelName: name });
  }

  const onModelListSet = (list: string[] | false) => {
    setModelList(list);
    if (!list || !list.length) {
      props.onModelSelect(undefined);
      return;
    }
    if (list.includes(modelName)) {
      props.onModelSelect({ raceId: props.raceId, modelName: modelName });
    } else {
      setModelName(list[0]);
      props.onModelSelect({ raceId: props.raceId, modelName: list[0] });
    }
  }

  if (!modelList) {
    return <Typography variant="body1"> Loading... </Typography>
  }
  if (!modelList.length) {
    return <Typography variant="body1"> No analysises exists. </Typography>
  }

  const handleTabChange = (_event: React.SyntheticEvent, newValue: string) => {
    onModelNameSet(newValue);
  };

  return (
    <>
      <Tabs
        value={modelName} onChange={handleTabChange} sx={{
          position: 'sticky',
          top: 96,
          zIndex: theme.zIndex.appBar,
          backgroundColor: theme.palette.background.default
        }}>
        {modelList.map(e => (
          <Tab key={e} value={e} label={getModelLabel(e)} />
        ))}
      </Tabs>
    </>
  )
}

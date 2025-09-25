import { useEffect, useState } from 'react';
import { Tab, Tabs, Typography } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { getModelList } from '../api';
import { Analysis } from './Analysis';
import { getModelLabel } from '../../models/types';


type Props = { raceId: string };

export function RaceAnalysises(props: Props) {

  const [model, setModel] = useState<string | false>(false);
  const [modelList, setModelList] = useState<string[] | false>(false);

  useEffect(() => {
    const previousModel = model;
    setModel(false)
    setModelList(false)
    const getList = async () => {
      const list = await getModelList(props.raceId);
      if (list.length) {
        if (previousModel && list.includes(previousModel)) {
          setModel(previousModel)
        } else {
          setModel(list[0])
        }
        setModelList(list)
      }
    }
    getList()
  }, [props.raceId])

  const handleTabChange = (_event: React.SyntheticEvent, newValue: string) => {
    setModel(newValue);
  };
  const theme = useTheme();

  return (
    <>
      {
        modelList ?
          <>
            <Tabs
              value={model} onChange={handleTabChange} sx={{
                position: 'sticky',
                top: 96,
                zIndex: theme.zIndex.appBar,
                backgroundColor: theme.palette.background.default
              }}>
              {modelList.map(e => (
                <Tab key={e} value={e} label={getModelLabel(e)} />
              ))}
            </Tabs>
            {
              model
                ? <Analysis key={`${props.raceId}-${model}`} raceId={props.raceId} modelName={model} />
                : null
            }
          </>
          : <Typography variant="body1"> Loading... </Typography>
      }
    </>
  )
}

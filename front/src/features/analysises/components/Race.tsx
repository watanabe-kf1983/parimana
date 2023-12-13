import { Button, Typography } from '@mui/material';
import { AnalysisStatus, RaceProps } from '../types';
import { useState, useEffect } from 'react';
import api from '../api/';
import { RaceAnalysises } from './RaceAnalysises';


export function Race(props: RaceProps) {

  const [status, setStatus] = useState<AnalysisStatus>({ "is_processing": false, "has_result": false })
  const [time, setTime] = useState<Date>(new Date())
  const refresh = () => setTime(new Date());

  const requestAnalyse = async () => {
    setStatus({is_processing: true, has_result: status.has_result})
    await api.requestAnalyse(props.raceId);
    refresh();
  };

  useEffect(() => {
    const getStatus = async () => {
      const s = await api.getAnalysisStatus(props.raceId);
      setStatus(s)
    }
    getStatus()
  }, [props.raceId, time]);

  return (
    <>
      <Typography variant="h2">
        for {props.raceId}
      </Typography>
      <Button onClick={refresh}> Refresh </Button>
      {status.has_result ?
        <RaceAnalysises raceId={props.raceId} />
        :
        <>
          <Button onClick={requestAnalyse}> Request Analyse </Button>
        </>
      }

    </>
  )
}

import { Button, Typography } from '@mui/material';
import { AnalysisStatus, RaceAnalysisesProps } from '../types';
import { Analysis } from './Analysis';
import { useState, useEffect } from 'react';
import { getAnalysisStatus } from '../api';


export function RaceAnalysises(props: RaceAnalysisesProps) {

  const [status, setStatus] = useState<AnalysisStatus>({ "is_processing": false, "has_result": false })

  useEffect(() => {
    const getStatus = async () => {
      const s = await getAnalysisStatus(props.raceId);
      setStatus(s)
    }
    getStatus()
  }, [props.raceId])

  return (
    <>
      <Typography variant="h2">
        RaceAnalysis
      </Typography>
      <Typography variant="body1">
        for {props.raceId}
      </Typography>
      {status.has_result ?
        <>
          <Analysis raceId={props.raceId} modelName="no_cor" />
          <Analysis raceId={props.raceId} modelName="ppf_mtx" />
        </>
        :
        <>
          <Button onClick={() => { }}> Request Analyse </Button>
        </>
      }

    </>
  )
}

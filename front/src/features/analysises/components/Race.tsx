import { Button } from '@mui/material';
import { AnalysisStatus, RaceProps } from '../types';
import { useState, useEffect } from 'react';
import api from '../api/';
import { RaceAnalysises } from './RaceAnalysises';


export function Race(props: RaceProps) {
  const initialStatus: AnalysisStatus = {
    "is_processing": false, "has_analysis": false, "is_odds_confirmed": false
  }
  const [status, setStatus] = useState<AnalysisStatus>(initialStatus)
  const [time, setTime] = useState<Date>(new Date())
  const reload = () => setTime(new Date());

  const requestAnalyse = async () => {
    setStatus({ is_processing: true, has_analysis: status.has_analysis, is_odds_confirmed: status.is_odds_confirmed })
    await api.requestAnalyse(props.raceId);
    reload();
  };

  useEffect(() => {
    const getStatus = async () => {
      const s = await api.getAnalysisStatus(props.raceId);
      setStatus(s)
    }
    getStatus()
  }, [props.raceId, time]);

  const requestButtonText = status.is_processing ? "Processing..." : (
    status.has_analysis ? "Request update odds & re-analyse" : "Request analyse"
  )

  return (
    <>
      {!status.is_odds_confirmed
        ? <>
          <Button variant="outlined" onClick={requestAnalyse} disabled={status.is_processing}>
            {requestButtonText}
          </Button>
          <Button variant="outlined" onClick={reload}> Reload </Button>
        </>
        : <></>}
      {status.has_analysis
        ? <RaceAnalysises raceId={props.raceId} />
        : <></>}
    </>
  )
}

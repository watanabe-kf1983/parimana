import { useState, useEffect } from 'react'
import { Link, Typography } from '@mui/material';
import { AnalysisProps, AnalysisData } from '../types';
import { Betting } from './Betting';
import { PlotlyChart } from './PlotlyChart';
import { Competences } from './Competences';
import { Simulation } from './Simulation';
import { getAnalysis } from '../api';

export function Analysis(props: AnalysisProps) {

  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);


  useEffect(() => {
    const getAn = async () => {
      const r = await getAnalysis(props.raceId, props.modelName);
      setAnalysis(r)
    }
    getAn()
  }, [props.raceId])

  return (
    <>
      <br />
      <br />
      {analysis
        ? <>
          <Typography variant="body1">
            Analysis of odds {analysis.odds_update_time}, <br />
            sourced from <Link target="_blank" href={analysis.source_uri}>{analysis.source_uri}</Link>
          </Typography>
          <hr />
          <Typography variant="h5">
            In '{props.modelName}' model:
          </Typography>
          <Competences competences={analysis.competences} chart={analysis.model_box} />
          <Simulation raceId={props.raceId} modelName={props.modelName} chart={analysis.odds_chance} />
        </>
        : <Typography variant="body1">
          Loading...
        </Typography>
      }
    </>
  );
}

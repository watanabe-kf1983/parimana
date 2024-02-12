import { useState, useEffect } from 'react'
import { Link, Typography } from '@mui/material';
import { AnalysisProps, Analysis } from '../types';
import { Recommendation } from './Recommendation';
import { PlotlyChart } from './PlotlyChart';
import { getAnalysis } from '../api';

export function Analysis(props: AnalysisProps) {

  const [analysis, setAnalysis] = useState<Analysis | null>(null);


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
      <Typography component="h4" variant="h4">
        Model: {props.modelName}
      </Typography>
      {analysis
        ? <>
          <Typography variant="body1">
            by analyzing the odds <b>{analysis.odds_update_time}</b>,
            Source: <Link target="_blank" href={analysis.source_uri}>{analysis.source_uri}</Link>
          </Typography>
          <Recommendation data={analysis.eev} />
          <PlotlyChart chartJSON={analysis.model_box} />
          <PlotlyChart chartJSON={analysis.odds_chance} />
        </>
        : <Typography variant="body1">
          Loading...
        </Typography>
      }
    </>
  );
}

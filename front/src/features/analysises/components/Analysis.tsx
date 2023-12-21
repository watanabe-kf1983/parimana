import { useState, useEffect } from 'react'
import { Typography } from '@mui/material';
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

  if (analysis == null) {
    return (
      <>
        <Typography component="h5" variant="h5">
          Model: {props.modelName}
        </Typography>
        <Typography variant="body1">
          Loading...
        </Typography>
      </>
    );
  } else {
    return (
      <>
        <Typography component="h5" variant="h5">
          Model: {props.modelName}
        </Typography>
        <PlotlyChart chartJSON={analysis.model_box} />
        <PlotlyChart chartJSON={analysis.odds_chance} />
        <Recommendation data={analysis.eev} />
      </>
    )
  }
}

import { useState, useEffect } from 'react'
import { Typography } from '@mui/material';
import { AnalysisProps, Recommend } from '../types';
import { Recommendation } from './Recommendation';
import { getBoxPlotUri, getOddsChartUri, getRecommendation } from '../api';
import styles from '../styles/Analysis.module.css';

export function Analysis(props: AnalysisProps) {

  const [recommendation, setRecommendation] = useState<Array<Recommend> | null>(null);
  const boxPlotUri = getBoxPlotUri(props.raceId, props.modelName);
  const oddsChartUri = getOddsChartUri(props.raceId, props.modelName);

  useEffect(() => {
    const getReco = async () => {
      const r = await getRecommendation(props.raceId, props.modelName);
      setRecommendation(r)
    }
    getReco()
  }, [props.raceId])

  if (recommendation == null) {
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
        <p>
          <img src={boxPlotUri} className={styles.responsiveImage} />
        </p>
        <Recommendation data={recommendation} />
        <p>
          <img src={oddsChartUri} className={styles.responsiveImage} />
        </p>
      </>
    )
  }
}

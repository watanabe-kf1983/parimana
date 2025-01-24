import { useState, useEffect } from 'react'
import { Box, Link, Typography } from '@mui/material';
import { AnalysisProps, AnalysisData } from '../types';
import { Competences } from './Competences';
import { Simulation } from './Simulation';
import { getAnalysis } from '../api';
import { Correlation } from './Correlation';

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
      <Box sx={{ m: 2 }}>
        {analysis
          ? <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
              オッズ情報源
            </Typography>
            <Typography variant="body1">
              <Link target="_blank" href={analysis.source_uri}>{analysis.source_uri}</Link>
              （{analysis.odds_update_time === "confirmed" ? "確定オッズ" : analysis.odds_update_time.replace("updated at ", "") + " 更新オッズ"}）
              <br />
              <br />
            </Typography>
            <Competences competences={analysis.competences} chart={analysis.model_box} />
            {props.modelName !== 'no_cor' ?
              <Correlation chart={analysis.model_mds} correlations={analysis.correlations} />
              : null
            }
            <Simulation raceId={props.raceId} modelName={props.modelName} chart={analysis.odds_chance} />
          </>
          : <Typography variant="body1">
            Loading...
          </Typography>
        }
      </Box>
    </>
  );
}

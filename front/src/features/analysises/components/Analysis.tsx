import { useState, useEffect } from 'react'
import { Box, Link, Typography } from '@mui/material';
import { Simulation } from '../../simulation/components/Simulation';
import { Model } from '../../models/components/Model';
import { AnalysisData } from '../types';
import { getAnalysis } from '../api';

type Props = { raceId: string, modelName: string };

export function Analysis(props: Props) {

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
            <SourceInfo uri={analysis.source_uri} updateTime={analysis.odds_update_time} />
            <br />
            <Model modelName={props.modelName}
              competences={analysis.competences}
              competencesChart={analysis.model_box}
              correlations={analysis.correlations}
              correlationsChart={analysis.model_mds} />
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


function SourceInfo(props: { uri: string, updateTime: string }) {

  return (
    <>
      <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
        オッズ情報源
      </Typography>
      <Typography variant="body1">
        <Link target="_blank" href={props.uri}>{props.uri}</Link>
        （{props.updateTime === "confirmed" ? "確定オッズ" : props.updateTime.replace("updated at ", "") + " 更新オッズ"}）
      </Typography>
    </>
  );
}

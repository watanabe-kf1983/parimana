import { useState, useEffect } from 'react'
import { Box, Link, Typography } from '@mui/material';
import { Simulation } from '../../simulation/components/Simulation';
import { Model } from '../../models/components/Model';
import { AnalysisData, SourceData } from '../types';
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
            <SourceInfo source={analysis.source} />
            <br />
            <Model model={analysis.model} />
            <Simulation raceId={props.raceId} modelName={props.modelName} chart={analysis.simulation.odds_chance_chart} />
          </>
          : <Typography variant="body1">
            Loading...
          </Typography>
        }
      </Box>
    </>
  );
}


function SourceInfo(props: { source: SourceData }) {
  const updateTime = props.source.odds_update_time
  const uri = props.source.source_uri

  return (
    <>
      <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
        オッズ情報源
      </Typography>
      <Typography variant="body1">
        <Link target="_blank" href={uri}>{uri}</Link>
        （{updateTime === "confirmed" ? "確定オッズ" : updateTime.replace("updated at ", "") + " 更新オッズ"}）
      </Typography>
    </>
  );
}

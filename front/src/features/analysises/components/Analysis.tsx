import { useState, useEffect } from 'react'
import { Box, Link, Typography } from '@mui/material';
import { Simulation } from '../../simulation/components/Simulation';
import { Model } from '../../models/components/Model';
import { AnalysisData, ModelKey, SourceData } from '../types';
import { getLatestAnalysis } from '../api';
import { LoadingOverlay } from '../../../common/components/LoadingOverlay';

type Props = { modelKey: ModelKey };

export function Analysis(props: Props) {

  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    const getAn = async () => {
      setFetching(true);
      try {
        const r = await getLatestAnalysis(props.modelKey);
        setAnalysis(r)
      } catch (e) {
        console.error(e)
      } finally {
        setFetching(false);
      }
    }
    getAn();
  }, [props.modelKey]);

  return (
    <Box m={2} sx={{ position: "relative" }}>
      {analysis &&
        <>
          <SourceInfo source={analysis.source} />
          <Model model={analysis.model} />
          <Simulation modelKey={props.modelKey} simulation={analysis.simulation} />
        </>
      }
      <LoadingOverlay loading={fetching} />
    </Box>

  );
}


function SourceInfo(props: { source: SourceData }) {
  const updateTime = props.source.odds_update_time.description
  const uri = props.source.source_uri

  return (
    <Box my={2} >
      <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
        オッズ情報源
      </Typography>
      <Typography variant="body1">
        <Link target="_blank" href={uri}>{uri}</Link>
        （{updateTime === "confirmed" ? "確定オッズ" : updateTime.replace("updated at ", "") + " 更新オッズ"}）
      </Typography>
    </Box>
  );
}



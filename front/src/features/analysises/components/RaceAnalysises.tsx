import { useState } from 'react';

import { Analysis } from './Analysis';
import { ModelKey } from '../types';
import { ModelSelector } from './ModelSelector';
import { Box } from '@mui/material';
import { LoadingOverlay } from '../../../common/components/LoadingOverlay';

type Props = { raceId: string };

export function RaceAnalysises(props: Props) {

  const [modelKey, setModelKey] = useState<ModelKey | undefined>(undefined);
  const [fetching, setFetching] = useState(false);

  return (
    <Box sx={{ position: "relative" }}>
      <ModelSelector raceId={props.raceId} onSetFetching={setFetching} onModelSelect={setModelKey} />
      {modelKey && <Analysis modelKey={modelKey} />}
      <LoadingOverlay loading={fetching} />
    </Box>
  )
}

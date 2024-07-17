import { Candidate, RecommendQueryProps } from '../types';
import { useEffect, useState } from 'react';
import { getRecommend } from '../api';
import { Candidates } from './Candidates';
import { QuerySelector } from './QuerySelector';
import { Typography } from '@mui/material';

export function Recommendation(props: RecommendQueryProps) {
  const [query, setQuery] = useState<string>("type=='TRIFECTA' and 10<odds<200 and expected>1");
  const [recs, setRecs] = useState<Candidate[]>([]);

  useEffect(() => {
    const getRecs = async () => {
      const r = await getRecommend(props.raceId, props.modelName, query);
      setRecs(r)
    }
    getRecs()
  }, [props.raceId, props.modelName, query])

  return (
    <>
      <QuerySelector onSetQuery={setQuery} query={query} />
      <br />
      <Typography component="h5" variant="h5">
        Reccommendations
      </Typography>
      <Candidates data={recs} />
    </>
  )
}

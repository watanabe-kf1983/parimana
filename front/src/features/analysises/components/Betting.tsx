import { Candidate, BettingQueryProps } from '../types';
import { useEffect, useState } from 'react';
import { getCandidates } from '../api';
import { Candidates } from './Candidates';
import { QuerySelector } from './QuerySelector';

export function Betting(props: BettingQueryProps) {
  const [query, setQuery] = useState<string>("");
  const [recs, setRecs] = useState<Candidate[]>([]);

  useEffect(() => {
    const getRecs = async () => {
      const r = await getCandidates(props.raceId, props.modelName, query);
      setRecs(r)
    }
    getRecs()
  }, [props.raceId, props.modelName, query])

  return (
    <>
      <QuerySelector onSetQuery={setQuery} query={query} />
      <Candidates data={recs} />
    </>
  )
}

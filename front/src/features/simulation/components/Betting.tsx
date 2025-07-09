import { useEffect, useState } from 'react';
import { Candidate } from '../types';
import { getCandidates } from '../api';
import { Candidates } from './Candidates';
import { QuerySelector } from './QuerySelector';

type Props = { raceId: string, modelName: string }

export function Betting(props: Props) {
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

import { useEffect, useState } from 'react';
import { Candidate } from '../types';
import { getCandidates } from '../api';
import { Candidates } from './Candidates';
import { QuerySelector } from './QuerySelector';
import { ModelKey } from '../../analysises/types';

type Props = { modelKey: ModelKey, timeId: string };

export function Betting(props: Props) {
  const [query, setQuery] = useState<string>("");
  const [recs, setRecs] = useState<Candidate[]>([]);

  useEffect(() => {
    const getRecs = async () => {
      const r = await getCandidates(props.modelKey, props.timeId, query);
      setRecs(r)
    }
    getRecs()
  }, [props.modelKey, props.timeId, query])

  return (
    <>
      <QuerySelector onSetQuery={setQuery} query={query} />
      <Candidates data={recs} />
    </>
  )
}

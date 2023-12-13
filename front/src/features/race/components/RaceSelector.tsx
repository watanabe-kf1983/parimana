import { useState } from 'react'
import { TextField } from '@mui/material';
import { RaceSelectorProps } from '../types';


export function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState(props.raceId)
  const selectRace = () => {
    props.onSetRaceId(raceId);
  }

  return (
    <>
      <TextField
        value={raceId}
        onChange={e => setRaceId(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            selectRace();
          }
        }}
        onBlur={selectRace} />
    </>
  )
}


import { useState } from 'react'
import { Button, TextField, Typography } from '@mui/material';
import { RaceSelectorProps } from '../types';


export function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState(props.raceId)

  return (
    <>
      <Typography variant="h2">
        Race Selector
      </Typography>
      {/* <FormControl> */}
      <TextField value={raceId} onChange={e => setRaceId(e.target.value)} />
      <Button onClick={() => props.onSetRaceId(raceId)}> See Analysis </Button>
      {/* </FormControl> */}
    </>
  )
}


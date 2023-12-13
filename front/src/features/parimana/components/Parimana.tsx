import { Typography } from "@mui/material"
import { useState } from "react"
import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"

export function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
      <Typography variant="h3">
        parimana: PARI-Mutuel odds ANAlyser
      </Typography>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
      <Race raceId={raceId} />
    </>
  )
}


import { Typography } from "@mui/material"
import { useState } from "react"
import { RaceAnalysises } from "../../analysises/components/RaceAnalysises"
import { RaceSelector } from "../../race/components/RaceSelector"

export function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
      <Typography variant="h1">
        parimana
      </Typography>
      <Typography variant="body1">
        PARI-Mutuel odds ANAlyser
      </Typography>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
      <RaceAnalysises raceId={raceId} />
    </>
  )
}


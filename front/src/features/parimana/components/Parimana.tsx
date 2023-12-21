import { Typography } from "@mui/material"
import { useState } from "react"
import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"
import mathJaxURL from "mathjax-full/es5/tex-svg.js?url"
import { MathJaxContext } from "better-react-mathjax"

export function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
      <MathJaxContext src={mathJaxURL}>
        <Typography variant="h3">
          parimana
        </Typography>
        <Typography variant="body1">
          PARI-Mutuel odds ANAlyser
        </Typography>
        <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
        <Race raceId={raceId} />
      </MathJaxContext>
    </>
  )
}


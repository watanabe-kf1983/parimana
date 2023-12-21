import { Typography } from "@mui/material"
import { useState } from "react"
import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"
import { MathJaxContext } from "better-react-mathjax"

// https://github.com/fast-reflexes/better-react-mathjax/issues/44#issuecomment-1589603608
import mathJaxURL from "mathjax-full/es5/tex-svg.js?url"

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


import { useParams, useNavigate } from 'react-router-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MathJaxContext } from "better-react-mathjax"

import { Box, Typography } from "@mui/material"

import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"

// https://github.com/fast-reflexes/better-react-mathjax/issues/44#issuecomment-1589603608
import mathJaxURL from "mathjax-full/es5/tex-svg.js?url"

export function Parimana() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ParimanaPage />} />
        <Route path="/analysis/:raceId" element={<ParimanaPage />} />
      </Routes>
    </BrowserRouter>
  )
}

function ParimanaPage() {
  return <ParimanaLayout content={<ParimanaContent />} />
}

function ParimanaLayout(props: { content: React.ReactNode }) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
      }}
    >
      <Box
        sx={{
          maxWidth: '1000px',
        }}
      >
        <Typography variant="h3">
          parimana
        </Typography>
        <Typography variant="body1">
          PARI-Mutuel odds ANAlyser
        </Typography>

        {props.content}

      </Box>
    </Box>
  )
}

function ParimanaContent() {
  const raceId = useParams().raceId || '';
  const navigate = useNavigate();
  const setRaceId = (raceId: string) => {
    navigate(`/analysis/${raceId}`);
  };

  return (
    <MathJaxContext src={mathJaxURL}>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
      <Race raceId={raceId} />
    </MathJaxContext>
  )
}

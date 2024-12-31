import { useParams, useNavigate } from 'react-router-dom';
import { Link as RouterLink } from "react-router-dom";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MathJaxContext } from "better-react-mathjax"

import { Box, Typography } from "@mui/material"

import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"

// https://github.com/fast-reflexes/better-react-mathjax/issues/44#issuecomment-1589603608
import mathJaxURL from "mathjax-full/es5/tex-svg.js?url"
import { HelpIcon } from './HelpIcon'
import { HelpContent } from './HelpContent';

export function Parimana() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ParimanaPage showControl={false} />} />
        <Route path="/sctl" element={<ParimanaPage showControl={true} />} />
        <Route path="/about" element={<HelpPage />} />
        <Route path="/analysis/:raceId" element={<ParimanaPage showControl={false} />} />
        <Route path="/analysis/:raceId/sctl" element={<ParimanaPage showControl={true} />} />
      </Routes>
    </BrowserRouter>
  )
}

function ParimanaPage(props: { showControl: boolean }) {
  return <ParimanaLayout content={<ParimanaContent showControl={props.showControl} />} />
}

function HelpPage() {
  return <ParimanaLayout content={<HelpContent />} />
}

function ParimanaLayout(props: { content: React.ReactNode }) {
  return (
    <MathJaxContext src={mathJaxURL}>
      <Box sx={{
        display: 'flex',
        justifyContent: 'center',
        padding: '10px',
        minHeight: '100vh',
        // minWidth: '1000px', // 最小幅をコンテンツの幅に合わせる
      }}
      >
        <Box sx={{
          maxWidth: '1030px'
        }}
        >
          <ParimanaHeader />
          {props.content}
        </Box>
      </Box>
    </MathJaxContext>
  )
}


function ParimanaHeader() {
  return (
    <>
      <Box sx={{ display: 'flex', flexDirection: 'row', m: 2 }}>
        <Typography
          component={RouterLink} to="/"
          variant="h3"
          sx={{
            color: "inherit",
            textDecoration: "none",
          }}>
          parimana
        </Typography>
        <Typography variant="body1" sx={{ m: 1 }}>
          PARI-Mutuel odds ANAlyser
        </Typography>
        <HelpIcon />
      </Box>
    </>
  )
}


function ParimanaContent(props: { showControl: boolean }) {
  const raceId = useParams().raceId || '';
  const navigate = useNavigate();
  const setRaceId = (raceId: string) => {
    navigate(props.showControl ? `/analysis/${raceId}/sctl` : `/analysis/${raceId}`);
  };

  return (
    <Box key={`parimana-content-${raceId}-${props.showControl}`}
      sx={{
        display: 'flex',
        flexDirection: 'column',
      }}>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} showControl={props.showControl} />
      {raceId ?
        <Race raceId={raceId} showControl={props.showControl} /> : null}
    </Box>
  )
}

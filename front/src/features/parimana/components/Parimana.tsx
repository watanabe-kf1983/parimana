import { useParams, useNavigate } from 'react-router-dom';
import { Link as RouterLink } from "react-router-dom";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MathJaxContext } from "better-react-mathjax"

import { Link, Box, Typography } from "@mui/material"

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
        <Route path="/" element={<ParimanaPage />} />
        <Route path="/about" element={<HelpPage />} />
        <Route path="/analysis/:raceId" element={<ParimanaPage />} />
      </Routes>
    </BrowserRouter>
  )
}

function ParimanaPage() {
  return <ParimanaLayout content={<ParimanaContent />} />
}

function HelpPage() {
  return <ParimanaLayout content={<HelpContent />} />
}

function ParimanaLayout(props: { content: React.ReactNode }) {

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        padding: '10px',
        minHeight: '100vh',
        // minWidth: '1000px', // 最小幅をコンテンツの幅に合わせる
      }}
    >
      <Box
        sx={{
          maxWidth: '1030px'
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            m: 2
          }}
        >
          {/* <Link href="/" variant="h3"> */}
          <Typography component={RouterLink} to="/" variant="h3" sx={{
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
        {props.content}

      </Box>
    </Box >
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
      <Box sx={{
        display: 'flex',
        flexDirection: 'column',
      }}>
        <div key={`parimana-content-${raceId}`}>
          <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
          <Race raceId={raceId} showControl={false} />
        </div>
      </Box>
    </MathJaxContext>
  )
}

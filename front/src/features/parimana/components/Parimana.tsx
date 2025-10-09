import { useParams, useNavigate } from 'react-router-dom';
import { Link as RouterLink } from "react-router-dom";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MathJaxContext } from "better-react-mathjax"

import { useTheme } from '@mui/material/styles';
import { Box, Typography } from "@mui/material"

import { Race } from "../../analysises/components/Race"
import { RaceSelector } from "../../race/components/RaceSelector"
import { useWindowSize } from '../../../common/hooks/useWindowSize';

// https://github.com/fast-reflexes/better-react-mathjax/issues/44#issuecomment-1589603608
import mathJaxURL from "mathjax-full/es5/tex-svg.js?url"
import { HelpIcon } from './HelpIcon'
import { HelpContent } from './HelpContent';
import { useEffect, useState } from 'react';
import api from '../api';

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
    <MathJaxContext src={mathJaxURL}>
      <Box sx={{
        display: 'flex',
        justifyContent: 'center',
        padding: '10px',
        minHeight: '100vh',
      }}
      >
        <Box sx={{
          maxWidth: '1030px',
          minWidth: `${Math.min(useWindowSize(), 1030)}px`,
        }}>
          <ParimanaHeader />
          {props.content}
        </Box>
      </Box>
    </MathJaxContext >
  )
}


function ParimanaHeader() {
  const theme = useTheme();

  return (
    <>
      <Box sx={{
        display: 'flex',
        flexDirection: 'row',
        m: 2,
        position: 'sticky',
        top: 0,
        zIndex: theme.zIndex.appBar,
        backgroundColor: theme.palette.background.default
      }}>
        <Typography
          component={RouterLink} to="/"
          variant="h3"
          sx={{
            color: "inherit",
            backgroundColor: "inherit",
            textDecoration: "none",
          }}>
          parimana
        </Typography>
        <Typography variant="body1" sx={{ m: 1 }}>
          PARI-Mutuel odds ANAlyser
        </Typography>
        <HelpIcon />
      </Box >
    </>
  )
}


function ParimanaContent() {
  const initialRaceId = useParams().raceId || undefined;
  const navigate = useNavigate();
  const [showControl, setShowControl] = useState<boolean>(false);
  const [raceSelected, setRaceSelected] = useState<boolean>(true);
  const [raceId, setRaceId] = useState<string | undefined>(initialRaceId);

  useEffect(() => {
    const getAppInfo = async () => {
      const appInfo = await api.getAppInfo();
      setShowControl(!appInfo.auto_analyse);
    };
    getAppInfo();
  }, []);

  if (!initialRaceId && raceSelected) {
    setRaceSelected(false);
  }

  const onSetRaceId = (rid: string) => {
    setRaceId(rid)
    setRaceSelected(true);
    navigate(`/analysis/${rid}`);
  };

  const clearRaceId = () => {
    setRaceSelected(false)
  };


  const theme = useTheme();

  return (
    <>
      <Box
        sx={{
          position: 'sticky',
          top: 56,
          zIndex: theme.zIndex.appBar,
          backgroundColor: theme.palette.background.default
        }}>
        <RaceSelector
          initialRaceId={initialRaceId}
          showControl={showControl}
          onSetRaceId={onSetRaceId}
          onClearRaceId={clearRaceId}
        />
      </Box>
      {
        raceId && (
          <Box sx={{ display: !raceSelected ? "none" : undefined }}>
            <Race raceId={raceId} showControl={showControl} />
          </Box>
        )
      }
    </>
  )
}

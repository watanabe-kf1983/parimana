import { useState, useEffect, useRef } from 'react';
import { Box, Typography } from '@mui/material';
import { RaceProps } from '../types';
import { getProgress } from '../api';

export function AnalysisProgress(props: RaceProps): JSX.Element {
  const [messages, setMessages] = useState<String>("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const progressManager = getProgress(props.raceId);

    progressManager.startListening((newMessage) => {
      setMessages((prevMessages) => `${prevMessages}\n${newMessage}`);
      if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
      }
    });

    return () => progressManager.stopListening();
  }, []);


  return (
    <Box ref={scrollRef} sx={{ height: 400, overflowY: 'scroll' }}>
      <Typography component="pre" variant="body1">
        {messages}
      </Typography>
    </Box>
  )
}

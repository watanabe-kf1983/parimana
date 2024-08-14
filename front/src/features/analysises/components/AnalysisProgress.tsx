import { useState, useEffect, useRef } from 'react';
import { Box, Typography } from '@mui/material';
import { AnalysisProgressProps } from '../types';
import { getProgress } from '../api';

export function AnalysisProgress(props: AnalysisProgressProps): JSX.Element {
  const [messages, setMessages] = useState<String>("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const progressManager = getProgress(props.raceId);

    const messageListener = (newMessage: string) => {
      setMessages((prevMessages) => `${prevMessages}\n${newMessage}`);
      if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
      }
    }

    progressManager.startListening(messageListener, props.onComplete, props.onAbort);

    return () => progressManager.stopListening();
  }, []);


  return (
    <Box ref={scrollRef} sx={{ height: 400, width: "100%", overflowY: 'scroll' }}>
      <Typography component="pre" variant="body1">
        {messages}
      </Typography>
    </Box>
  )
}

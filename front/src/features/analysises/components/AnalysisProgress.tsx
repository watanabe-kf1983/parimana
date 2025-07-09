import { useState, useEffect, useRef } from 'react';
import { Box, Typography } from '@mui/material';
import { getProgress } from '../api';

type Props = { raceId: string, onComplete: () => void, onAbort: () => void };

export function AnalysisProgress(props: Props): JSX.Element {
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
    <Box ref={scrollRef} sx={{ width: "100%" }}>
      <Typography component="pre" variant="body1">
        {messages}
      </Typography>
    </Box>
  )
}

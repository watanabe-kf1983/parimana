import { useState, useEffect } from 'react';
import { Typography } from '@mui/material';
import { RaceProps } from '../types';
import { getProgress } from '../api';

export function AnalysisProgress(props: RaceProps): JSX.Element {
  const [messages, setMessages] = useState<String>("");

  useEffect(() => {
    const progressManager = getProgress(props.raceId);

    progressManager.startListening((newMessage) => {
      setMessages((prevMessages) => `${prevMessages}\n${newMessage}`);
    });

    return () => progressManager.stopListening();
  }, []);


  return (
    <Typography component="pre" variant="body1">
      {messages}
    </Typography>
  )
}

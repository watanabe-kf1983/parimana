import { Box } from "@mui/material";
import { AnalysisStatus, RaceProps } from "../types";
import { useState, useEffect } from "react";
import api from "../api";
import { RaceAnalysises } from "./RaceAnalysises";
import { AnalyseControl } from "./AnalyseControl";
import { AnalysisProgress } from "./AnalysisProgress";

export function Race(props: RaceProps) {
  const initialStatus: AnalysisStatus = {
    is_processing: false,
    has_analysis: false,
    is_odds_confirmed: false,
  };
  const [status, setStatus] = useState<AnalysisStatus>(initialStatus);
  const [time, setTime] = useState<Date>(new Date());
  const reload = () => setTime(new Date());

  useEffect(() => {
    const getStatus = async () => {
      if (props.raceId) {
        const s = await api.getAnalysisStatus(props.raceId);
        setStatus(s);
      }
    };
    getStatus();
  }, [props.raceId, time]);

  if (!props.raceId) {

    return null;

  } else {

    return (
      <>
        <Box sx={{
          display: 'flex',
          flexDirection: 'row',
        }}>
          {props.showControl ? (
            <>
              <AnalyseControl
                raceId={props.raceId}
                status={status}
                onReload={reload}
              />
            </>
          ) : null}
        </Box>
        {props.showControl && status.is_processing ? (
          <AnalysisProgress
            raceId={props.raceId}
            onComplete={reload}
            onAbort={() => { }}
          />
        ) : null}
        {status.has_analysis && (!status.is_processing || !props.showControl) ? (
          <RaceAnalysises raceId={props.raceId} />
        ) : null}
      </>
    );
  }

}

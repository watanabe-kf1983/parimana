import { useState, useEffect } from "react";
import { Box } from "@mui/material";

import { AnalysisStatus } from "../types";
import api from "../api";
import { RaceAnalysises } from "./RaceAnalysises";
import { AnalyseControl } from "./AnalyseControl";
import { AnalysisProgress } from "./AnalysisProgress";
import { LoadingOverlay } from "../../../common/components/LoadingOverlay";

type Props = { raceId: string | undefined, showControl: boolean };

export function Race(props: Props) {
  const initialStatus: AnalysisStatus = {
    is_processing: false,
    has_analysis: false,
    is_odds_confirmed: false,
  };
  const [status, setStatus] = useState<AnalysisStatus>(initialStatus);
  const [time, setTime] = useState<Date>(new Date());
  const [fetching, setFetching] = useState(false);
  const reload = () => setTime(new Date());

  useEffect(() => {
    const getStatus = async () => {
      if (props.raceId) {
        setFetching(true);
        const s = await api.getAnalysisStatus(props.raceId);
        setStatus(s);
        setFetching(false);
      }
    };
    getStatus();
  }, [props.raceId, time]);

  if (!props.raceId) {
    return null;
  }

  return (
    <>
      <Box sx={{ position: "relative" }}>
        <Box sx={{
          display: 'flex',
          flexDirection: 'row',
        }}>
          {props.showControl && (
            <>
              <AnalyseControl
                raceId={props.raceId}
                status={status}
                onReload={reload}
              />
            </>
          )}
        </Box>
        {props.showControl && status.is_processing && (
          <AnalysisProgress
            raceId={props.raceId}
            onComplete={reload}
            onAbort={() => { }}
          />
        )}
        {status.has_analysis && !(status.is_processing && props.showControl) && (
          <RaceAnalysises raceId={props.raceId} />
        )}
        <LoadingOverlay loading={fetching} />
      </Box>
    </>
  );

}

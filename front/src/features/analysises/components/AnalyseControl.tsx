import { Button } from "@mui/material";
import { AnalyseControlProps } from "../types";
import api from "../api/";

export function AnalyseControl(props: AnalyseControlProps) {

  const status = props.status;

  const requestAnalyse = async () => {
    await api.requestAnalyse(props.raceId);
    props.onReload();
  };


  return (
    <>
      {!status.is_odds_confirmed && !status.is_processing ? (
        <Button
          variant="outlined"
          onClick={requestAnalyse}
          disabled={false}
        >
          {status.has_analysis
            ? "Request update odds & re-analyse"
            : "Request analyse"}
        </Button>
      ) : null
      }
      {status.is_processing ? (
        <>
          <Button
            variant="outlined"
            onClick={() => { }}
            disabled={true}
          >
            Processing...
          </Button>
        </>
      ) : null}
    </>
  );
}

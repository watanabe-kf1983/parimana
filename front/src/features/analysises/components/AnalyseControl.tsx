import { Button } from "@mui/material";
import { AnalyseControlProps } from "../types";
import api from "../api/";

export function AnalyseControl(props: AnalyseControlProps) {

  const status = props.status;

  const requestAnalyse = async () => {
    await api.requestAnalyse(props.raceId);
    await new Promise(resolve => setTimeout(resolve, 100));
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
            ? "オッズ更新＆再計算"
            : "オッズ取得＆計算"}
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
            処理中...
          </Button>
        </>
      ) : null}
    </>
  );
}

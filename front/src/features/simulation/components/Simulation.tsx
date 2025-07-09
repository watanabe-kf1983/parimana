import { Typography } from '@mui/material';

import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { Betting } from './Betting';

type Props = { raceId: string, modelName: string, chart: string };

export function Simulation(props: Props) {

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                的中確率と払戻期待値
            </Typography>
            <Betting raceId={props.raceId} modelName={props.modelName} />
            <PlotlyChart chartJSON={props.chart} />
        </>
    )
}

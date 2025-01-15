import { Typography } from '@mui/material';

import { SimulationProps } from '../types';
import { PlotlyChart } from './PlotlyChart';
import { Betting } from './Betting';


export function Simulation(props: SimulationProps) {

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

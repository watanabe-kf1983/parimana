import { Typography } from '@mui/material';

import { SimulationProps } from '../types';
import { PlotlyChart } from './PlotlyChart';
import { Betting } from './Betting';


export function Simulation(props: SimulationProps) {

    return (
        <>
            <Typography variant="h6">
                Expected dividends by simulation
            </Typography>
            <Betting raceId={props.raceId} modelName={props.modelName} />
            <PlotlyChart chartJSON={props.chart} />
        </>
    )
}

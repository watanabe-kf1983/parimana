import { Typography } from '@mui/material';

import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { ModelKey } from '../../analysises/types';
import { Betting } from './Betting';
import { SimulationData } from '../types';

type Props = { modelKey: ModelKey, simulation: SimulationData };

export function Simulation(props: Props) {
    const chart = props.simulation.odds_chance_chart;

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                的中確率と払戻期待値
            </Typography>
            <Betting modelKey={props.modelKey} timeId={props.simulation.odds_update_time.id} />
            {chart && <PlotlyChart chartJSON={chart} />}
        </>
    )
}

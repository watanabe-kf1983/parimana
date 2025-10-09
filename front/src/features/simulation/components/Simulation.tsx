import { Typography } from '@mui/material';

import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { ModelKey } from '../../analysises/types';
import { Betting } from './Betting';

type Props = { modelKey: ModelKey, chart: string };

export function Simulation(props: Props) {

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                的中確率と払戻期待値
            </Typography>
            <Betting modelKey={props.modelKey} />
            <PlotlyChart chartJSON={props.chart} />
        </>
    )
}

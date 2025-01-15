import { Typography } from '@mui/material';

import { CorrelationProps } from '../types';
import { PlotlyChart } from './PlotlyChart';

export function Correlation(props: CorrelationProps) {

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                出走者間の相関
            </Typography>
            <PlotlyChart chartJSON={props.chart} />
            <br></br>
        </>
    );
}

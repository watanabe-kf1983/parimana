import { Typography } from '@mui/material';
import { Competence } from '../types';
import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { CompetenceTable } from './CompetenceTable';

type Props = { competences: Array<Competence>, chart: string };

export function Competences(props: Props) {
    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                予想走破時計
            </Typography>
            <CompetenceTable competences={props.competences} />
            <PlotlyChart chartJSON={props.chart} />
            <br></br>
        </>
    );
}

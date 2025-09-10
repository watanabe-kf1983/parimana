import { Divider, Grid, Stack, Typography } from '@mui/material';
import { CompetencesByPlace, getPlaceLabel } from '../types';
import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { CompetenceTable } from './CompetenceTable';

type Props = { competences_by_places: Array<CompetencesByPlace>, chart: string };

export function CompetencesMulti(props: Props) {
    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                予想走破時計
            </Typography>
            <Stack spacing={2} divider={<Divider flexItem />} sx={{ width: '100%' }}>
                {props.competences_by_places.map((e) => (
                    <Grid container key={e.place}>
                        <Grid item xs={12} md={2}>
                            <Typography variant="h6">
                                {getPlaceLabel(e.place)}
                            </Typography>
                        </Grid>
                        <Grid item xs={12} md={10}>
                            <CompetenceTable competences={e.competences} />
                        </Grid>
                    </Grid>
                ))}
            </Stack>
            <PlotlyChart chartJSON={props.chart} />
        </>
    );
}

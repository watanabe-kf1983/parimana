import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';
import { Typography } from '@mui/material';
import { Competence } from '../types';
import { PlotlyChart } from '../../../common/components/PlotlyChart';

type Props = { competences: Array<Competence>, chart: string };

export function Competences(props: Props) {

    const rows: GridRowsProp = props.competences.map(rec => ({
        id: rec.contestant,
        contestant: rec.contestant,
        mean: rec.mean,
        q1: rec.q1,
        q3: rec.q3,
        sd: rec.sd
    }));


    const columns: GridColDef[] = [
        { field: 'contestant', headerName: '#', type: 'string', width: 20 },
        {
            field: 'mean', headerName: 'mean', type: 'number', width: 90,
            valueFormatter: (value: number) => `${value.toFixed(3)}`,
        },
        {
            field: 'sd', headerName: 'σ', type: 'number', width: 70,
            valueFormatter: (value: number) => `${value.toFixed(3)}`,
        },
        {
            field: 'q1', headerName: 'q1', type: 'number', width: 70,
            valueFormatter: (value: number) => `${value.toFixed(2)}`,
        },
        {
            field: 'q3', headerName: 'q3', type: 'number', width: 70,
            valueFormatter: (value: number) => `${value.toFixed(2)}`,
        },
    ];

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                予想走破時計
            </Typography>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <DataGrid rows={rows} columns={columns} density='compact'
                    disableColumnMenu hideFooter />
            </div>
            <PlotlyChart chartJSON={props.chart} />
            <br></br>
        </>
    );
}

import { Typography } from '@mui/material';
import { PlotlyChart } from '../../../common/components/PlotlyChart';
import { DataGrid, GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { CorrelationData } from '../types';

type Props = { correlations: Array<CorrelationData>, chart: string };

export function Correlation(props: Props) {


    const rows: GridRowsProp = props.correlations.map((c) => ({ id: c.a, ...c.row }));
    const bcolumns: GridColDef[] = props.correlations.map((c) => ({
        field: c.a,
        headerName: c.a,
        type: 'number',
        width: 55,
        valueFormatter: (value: number) => `${value.toFixed(2)}`
    }));
    const columns: GridColDef[] = [
        { field: 'id', headerName: '#', type: 'string', width: 40 },
        ...bcolumns
    ]

    return (
        <>
            <Typography variant="h5" gutterBottom sx={{ borderBottom: "thin solid" }}>
                出走者間の相関
            </Typography>
            <DataGrid rows={rows} columns={columns} density='compact'
                autoHeight disableColumnMenu hideFooter />
            <PlotlyChart chartJSON={props.chart} />
            <br></br>
        </>
    );
}

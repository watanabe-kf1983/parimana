import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';

import { CandidatesProps } from '../types';


export function Candidates(props: CandidatesProps) {


    const rows: GridRowsProp = props.data.map(rec => ({
        id: rec.eye.text,
        eye: rec.eye.text,
        type: rec.eye.type,
        odds: rec.odds,
        chance: rec.chance,
        expected: rec.expected
    }));

    const columns: GridColDef[] = [
        { field: 'eye', headerName: 'Betting', type: 'string' },
        {
            field: 'type', headerName: 'Type', type: 'singleSelect',
            valueOptions: ['WIN', 'PLACE', 'SHOW', 'EXACTA', 'QUINELLA', 'WIDE', 'TRIFECTA', 'TRIO']
        },
        {
            field: 'odds', headerName: 'Odds', type: 'number',
            valueFormatter: (value: number) => `${value.toFixed(1)}`
        },
        {
            field: 'chance', headerName: 'Chance', type: 'number',
            valueFormatter: (value: number) => `${(value * 100).toFixed(2)}%`
        },
        {
            field: 'expected', headerName: 'Expectation', type: 'number',
            valueFormatter: (value: number) => `${(value * 100).toFixed(2)}%`
        },
    ];

    return (
        <div style={{ maxWidth: '100%' }}>
            <DataGrid autoHeight rows={rows} columns={columns}
                density='compact' pageSizeOptions={[10, 25, 50]}
                initialState={{
                    pagination: { paginationModel: { pageSize: 10 } },
                }}
            // slots={{ toolbar: GridToolbar }}
            />
        </div>
    )
}

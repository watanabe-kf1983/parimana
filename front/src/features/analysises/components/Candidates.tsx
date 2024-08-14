import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';

import { CandidatesProps } from '../types';


export function Candidates(props: CandidatesProps) {


    const rows: GridRowsProp = props.data.map(rec => ({
        id: rec.eye.text,
        eye: rec.eye.text,
        type: rec.eye.type,
        odds: rec.odds.toFixed(1),
        chance: (rec.chance * 100).toFixed(2),
        expected: rec.expected.toFixed(4)
    }));

    const columns: GridColDef[] = [
        { field: 'eye', headerName: 'Bet', width: 100 },
        { field: 'odds', headerName: 'Odds', width: 100 },
        { field: 'chance', headerName: 'Chance', width: 100 },
        { field: 'expected', headerName: 'Expectation', width: 100 },
    ];

    return (
        <div style={{ height: 300, maxWidth: '400px' }}>
            <DataGrid rows={rows} columns={columns} />
        </div>
    )
}

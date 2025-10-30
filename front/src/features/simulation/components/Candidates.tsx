import { DataGrid, GridRowsProp, GridColDef } from '@mui/x-data-grid';
import { useWindowSize } from '../../../common/hooks/useWindowSize';
import { Candidate } from '../types';
import { getModelLabel } from '../../models/types';

type Props = { data: Array<Candidate> };

export function Candidates(props: Props) {

    const MAX_TABLE_WIDTH = 1000;
    const FRAME_PADDING = 15;
    const tableWidth = Math.min(useWindowSize() - FRAME_PADDING * 2, MAX_TABLE_WIDTH)

    const rec_row_mapper = (rec: Candidate) => {
        const row: any = {
            id: rec.eye.text,
            eye: rec.eye.text,
            type: rec.eye.type,
            odds: rec.odds,
            chance: rec.chance,
            expected: rec.expected
        }
        for (const otherField of rec.others) {
            row[otherField.name] = otherField.value;
        };
        return row;
    }

    const rows: GridRowsProp = props.data.map(rec_row_mapper);

    const columns: GridColDef[] = [
        { field: 'eye', headerName: 'Betting', type: 'string' },
        {
            field: 'type', headerName: 'Type', type: 'singleSelect',
            valueOptions: ['WIN', 'PLACE', 'SHOW', 'EXACTA', 'QUINELLA', 'WIDE', 'TRIFECTA', 'TRIO'],
        },
        {
            field: 'odds', headerName: 'Odds', type: 'number',
            valueFormatter: (value: number) => `${value.toFixed(1)}`,
        },
        {
            field: 'chance', headerName: 'Chance', type: 'number',
            valueFormatter: (value: number) => `${(value * 100).toFixed(2)}%`,
        },
        {
            field: 'expected', headerName: 'Expectation', type: 'number',
            valueFormatter: (value: number) => `${(value * 100).toFixed(2)}%`,
        },
    ];

    if (props.data.length > 0) {
        for (const otherField of props.data[0].others) {
            if (otherField.name.includes("_expected")) {
                columns.push({
                    field: otherField.name,
                    headerName: getModelLabel(otherField.name.replace("_expected", "")),
                    type: 'number',
                    valueFormatter: (value: number) => `${(value * 100).toFixed(2)}%`,
                });
            }
        }
    }

    return (
        <>
            <DataGrid autoHeight rows={rows} columns={columns}
                disableColumnMenu={tableWidth < 800}
                disableColumnSorting={tableWidth < 800}
                density='compact' pageSizeOptions={[10, 25, 50]}
                initialState={{
                    pagination: { paginationModel: { pageSize: 10 } },
                }}
                columnVisibilityModel={{
                    type: (tableWidth > 500),
                    odds: (tableWidth > 400),
                }}
            // sx={{ maxWidth: '100%' }}
            // slots={{ toolbar: GridToolbar }}
            />
        </>
    )
}

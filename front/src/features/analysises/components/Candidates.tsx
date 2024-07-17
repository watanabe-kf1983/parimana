import { Table, TableBody, TableHead, TableRow, TableCell } from '@mui/material';

import { CandidatesProps } from '../types';

export function Candidates(props: CandidatesProps) {
    return (
        <Table stickyHeader style={{ maxWidth: "400px" }}>
            <TableHead>
                <TableRow>
                    <TableCell>eye</TableCell>
                    <TableCell align="right">odds</TableCell>
                    <TableCell align="right">chance</TableCell>
                    <TableCell align="right">expected</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {props.data.map(rec => (
                    <TableRow>
                        <TableCell>{rec.eye.text}</TableCell>
                        <TableCell align="right">{rec.odds.toFixed(1)}</TableCell>
                        <TableCell align="right">{(rec.chance * 100).toFixed(2)}%</TableCell>
                        <TableCell align="right">{rec.expected.toFixed(4)}</TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}

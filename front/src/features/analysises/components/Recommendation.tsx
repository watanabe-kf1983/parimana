import { Table, TableBody, TableHead, TableRow, TableCell } from '@mui/material';
import { RecommendProps } from '../types';

export function Recommendation(props: RecommendProps) {
  const data = props.data

  return (
    <Table stickyHeader style={{ width: "400px" }}>
      <TableHead>
        <TableRow>
          <TableCell>eye</TableCell>
          <TableCell align="right">odds</TableCell>
          <TableCell align="right">chance</TableCell>
          <TableCell align="right">expected</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map(rec => (
          <TableRow>
            <TableCell>{rec.eye.text}</TableCell>
            <TableCell align="right">{rec.odds.toFixed(1)}</TableCell>
            <TableCell align="right">{rec.chance.toFixed(4)}</TableCell>
            <TableCell align="right">{rec.expected.toFixed(4)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table >
  )
}

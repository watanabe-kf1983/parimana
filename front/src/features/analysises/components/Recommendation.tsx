import { Table, TableBody, TableHead, TableRow, TableCell, Typography } from '@mui/material';
import { RecommendProps } from '../types';

export function Recommendation(props: RecommendProps) {
  const data = props.data

  return (
    <>
      <br />
      <Typography component="h5" variant="h5">
          Recommends:
      </Typography>
      <Table stickyHeader style={{ maxWidth: "600px" }}>
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
              <TableCell align="right">{(rec.chance*100).toFixed(2)}%</TableCell>
              <TableCell align="right">{rec.expected.toFixed(4)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <br />
    </>
  )
}

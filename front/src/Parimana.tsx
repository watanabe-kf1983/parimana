import { Dispatch, SetStateAction, useState, useEffect } from 'react'
import axios from 'axios'
import { Button, TextField, Table, TableBody, TableHead, TableRow, TableCell, Typography } from '@mui/material';

function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
      <Typography variant="h1">
        parimana
      </Typography>
      <Typography variant="body1">
        PARI-Mutuel odds ANAlyser
      </Typography>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
      <RaceAnalysises raceId={raceId} />
    </>
  )
}

type RaceSelectorProps = { raceId: string, onSetRaceId: Dispatch<SetStateAction<string>> }

function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState(props.raceId)

  return (
    <>
      <Typography variant="h2">
        Race Selector
      </Typography>
      {/* <FormControl> */}
      <TextField value={raceId} onChange={e => setRaceId(e.target.value)} />
      <Button onClick={() => props.onSetRaceId(raceId)}> Analyse </Button>
      {/* </FormControl> */}
    </>
  )
}

type RaceAnalysisesProps = { raceId: string }

function RaceAnalysises(props: RaceAnalysisesProps) {
  return (
    <>
      <Typography variant="h2">
        RaceAnalysis
      </Typography>
      <Typography variant="body1">
        for {props.raceId}
      </Typography>
      <Analysis raceId={props.raceId} modelName="no_cor" />
      <Analysis raceId={props.raceId} modelName="ppf_mtx" />
    </>
  )
}

type AnalysisProps = { raceId: string, modelName: string }


type Eye = { text: string, type: string }
type Recommend = { eye: Eye, odds: number, chance: number, expected: number }

function Analysis(props: AnalysisProps) {

  const [recommendation, setRecommendation] = useState<Array<Recommend> | null>(null)

  useEffect(() => {
    const getReco = async () => {
      const response = await axios.get(`http://127.0.0.1:5000/analysis/${props.raceId}/${props.modelName}`);
      setRecommendation(response.data)
    }
    getReco()
  }, [props.raceId])

  if (recommendation == null) {
    return (
      <>
        <Typography component="h3" variant="h3">
          Model: {props.modelName}
        </Typography>
        <Typography variant="body1">
          Loading...
        </Typography>
      </>
    );
  } else {
    return (
      <>
        <Typography component="h3" variant="h3">
          Model: {props.modelName}
        </Typography>
        <p>
          <img src={`http://127.0.0.1:5000/analysis/${props.raceId}/${props.modelName}/box.png`} style={{ width: "100%", height: "auto" }} />
        </p>
        <Recommendation data={recommendation} />
        <p>
          <img src={`http://127.0.0.1:5000/analysis/${props.raceId}/${props.modelName}/oc.png`} style={{ width: "100%", height: "auto" }} />
        </p>
      </>
    )
  }
}

type RecommendProps = { data: Array<Recommend> }

function Recommendation(props: RecommendProps) {
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


export default Parimana

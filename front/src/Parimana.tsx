import { Dispatch, SetStateAction, useState, useEffect } from 'react'
import axios from 'axios'
import { Button, Input, FormControl, Table, TableBody, TableHead, TableRow, TableCell, Typography } from '@mui/material';

function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
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
      <Typography component="h1" variant="h1">
        Race Selector
      </Typography>
      <FormControl>
        <Input value={raceId} onChange={e => setRaceId(e.target.value)} />
        <Button onClick={() => props.onSetRaceId(raceId)}> Analyse </Button>
      </FormControl>
    </>
  )
}

type RaceAnalysisesProps = { raceId: string }

function RaceAnalysises(props: RaceAnalysisesProps) {
  return (
    <>
      <Typography component="h1" variant="h1">
        RaceAnalysis 
      </Typography>
      for {props.raceId}
      <Analysis raceId={props.raceId} modelName="no_cor" />
      <Analysis raceId={props.raceId} modelName="ppf_mtx" />
    </>
  )
}

type AnalysisProps = { raceId: string, modelName: string }


type Recommend = { [key: string]: { type: string, odds: string, chance: string, expected: string } }

function Analysis(props: AnalysisProps) {

  const [recommendation, setRecommendation] = useState<Recommend | null>(null)

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
        <Typography component="h2" variant="h2">
          Model: {props.modelName}
        </Typography>
        Loading...
      </>
    );
  } else {
    return (
      <>
        <Typography component="h2" variant="h2">
          Model: {props.modelName}
        </Typography>
        <p>
          <img src={`http://127.0.0.1:5000/analysis/${props.raceId}/${props.modelName}/box.png`} style={{ width: "50%", height: "auto" }} />
        </p>
        <Recommendation data={recommendation} />
        <p>
          <img src={`http://127.0.0.1:5000/analysis/${props.raceId}/${props.modelName}/oc.png`} style={{ width: "100%", height: "auto" }} />
        </p>
      </>
    )
  }
}

type RecommendProps = { data: Recommend }

function Recommendation(props: RecommendProps) {
  const data = props.data

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>eye</TableCell>
          <TableCell>type</TableCell>
          <TableCell>odds</TableCell>
          <TableCell>chance</TableCell>
          <TableCell>expected</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {Object.keys(data).map(key => (
          <TableRow>
            <TableCell>{key}</TableCell>
            <TableCell>{data[key].type}</TableCell>
            <TableCell>{Number.parseFloat(data[key].odds).toFixed(4)}</TableCell>
            <TableCell>{Number.parseFloat(data[key].chance).toFixed(4)}</TableCell>
            <TableCell>{Number.parseFloat(data[key].expected).toFixed(4)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}


export default Parimana

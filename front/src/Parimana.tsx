import { Dispatch, SetStateAction, useState } from 'react'

function Parimana() {
  const [raceId, setRaceId] = useState("")

  return (
    <>
      <RaceSelector raceId={raceId} onSetRaceId={setRaceId} />
      <RaceAnalysis raceId={raceId} />
    </>
  )
}

type RaceSelectorProps = { raceId: string, onSetRaceId: Dispatch<SetStateAction<string>> }

function RaceSelector(props: RaceSelectorProps) {
  const [raceId, setRaceId] = useState(props.raceId)

  return (
    <>
      <h1>RaceSelector</h1>
      <input type="text" value={raceId} onChange={e => setRaceId(e.target.value)} />
      <button onClick={() => props.onSetRaceId(raceId)} />
    </>
  )
}

type RaceAnalysisProps = { raceId: string }

function RaceAnalysis(props: RaceAnalysisProps) {
  return (
    <>
      <h1>RaceAnalysis</h1>
      {props.raceId}
      {/* <img src={`img/${props.raceId}/ac.png`} /> */}
    </>
  )
}

export default Parimana

import { Dispatch, SetStateAction } from 'react'

export type Eye = { text: string, type: string }
export type Candidate = { eye: Eye, odds: number, chance: number, expected: number }

export type BettingProps = { raceId: string, modelName: string }
export type CandidatesProps = { data: Array<Candidate> }
export type QuerySelectorProps = { query: string, onSetQuery: Dispatch<SetStateAction<string>> }
export type SimulationProps = { raceId: string, modelName: string, chart: string }

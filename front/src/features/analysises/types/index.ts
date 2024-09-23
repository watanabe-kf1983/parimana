import { Dispatch, SetStateAction } from 'react'

export type RaceProps = { raceId: string }

export type AnalysisProgressProps = { raceId: string, onComplete: () => void, onAbort: () => void }

export type AnalysisProps = { raceId: string, modelName: string }
export type CompetenceProps = { competences: Array<Competence>, chart: string }

export type AnalysisStatus = { is_processing: boolean, has_analysis: boolean, is_odds_confirmed: boolean }

export type Eye = { text: string, type: string }

export type AnalysisData = {
    eev: Array<Recommend>,
    competences: Array<Competence>,
    source_uri: string,
    odds_update_time: string,
    odds_chance: string,
    model_box: string
}

export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }
export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }

export type BettingQueryProps = { raceId: string, modelName: string }

export type RecommendProps = { data: Array<Recommend> }

export type Candidate = { eye: Eye, odds: number, chance: number, expected: number }
export type CandidatesProps = { data: Array<Candidate> }

export type QuerySelectorProps = { query: string, onSetQuery: Dispatch<SetStateAction<string>> }

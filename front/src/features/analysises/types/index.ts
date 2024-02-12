export type RaceProps = { raceId: string }

export type AnalysisProgressProps = { raceId: string, onTerminate: () => void }

export type AnalysisProps = { raceId: string, modelName: string }

export type AnalysisStatus = { is_processing: boolean, has_analysis: boolean, is_odds_confirmed: boolean }

export type Eye = { text: string, type: string }

export type Analysis = {
    eev: Array<Recommend>,
    source_uri: string,
    odds_update_time: string,
    odds_chance: string,
    model_box: string
}

export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }

export type RecommendProps = { data: Array<Recommend> }

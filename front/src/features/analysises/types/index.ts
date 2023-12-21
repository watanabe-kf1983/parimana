export type RaceProps = { raceId: string }

export type AnalysisProps = { raceId: string, modelName: string }

export type AnalysisStatus = { is_processing: boolean, has_result: boolean }

export type Eye = { text: string, type: string }

export type Analysis = { eev: Array<Recommend>, odds_chance: string, model_box: string }

export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }

export type RecommendProps = { data: Array<Recommend> }

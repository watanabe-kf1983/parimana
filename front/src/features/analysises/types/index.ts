export type RaceAnalysisesProps = { raceId: string }

export type AnalysisProps = { raceId: string, modelName: string }

export type Eye = { text: string, type: string }

export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }

export type RecommendProps = { data: Array<Recommend> }

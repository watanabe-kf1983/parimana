import { ModelData } from "../../models/types"
import { SimulationData } from "../../simulation/types"

export type ModelKey = {
    raceId: string,
    modelName: string,
}
export type AnalysisStatus = { is_processing: boolean, has_analysis: boolean, is_odds_confirmed: boolean }
export type Eye = { text: string, type: string }
export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }
export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }
export type Correlation = { a: string, row: object }
export type AnalysisData = {
    source: SourceData,
    model: ModelData,
    simulation: SimulationData,
}
export type SourceData = {
    source_uri: string,
    odds_update_time: string,
}

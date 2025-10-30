import { ModelData } from "../../models/types"
import { SimulationData } from "../../simulation/types"

export type ModelKey = {
    raceId: string,
    modelName: string,
}
export type AnalysisStatus = { is_processing: boolean, has_analysis: boolean, is_odds_confirmed: boolean }
export type AnalysisData = {
    source: SourceData,
    model?: ModelData,
    simulation: SimulationData,
}
export type SourceData = {
    source_uri: string,
    odds_update_time: OddsUpdateTimeData,
}
export type OddsUpdateTimeData = {
    id: string,
    description: string,
}

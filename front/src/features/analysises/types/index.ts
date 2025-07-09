export type AnalysisStatus = { is_processing: boolean, has_analysis: boolean, is_odds_confirmed: boolean }
export type Eye = { text: string, type: string }
export type Recommend = { eye: Eye, odds: number, chance: number, expected: number }
export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }
export type Correlation = { a: string, row: object }
export type AnalysisData = {
    eev: Array<Recommend>,
    competences: Array<Competence>,
    correlations: Array<Correlation>,
    source_uri: string,
    odds_update_time: string,
    odds_chance: string,
    model_box: string,
    model_mds: string,
}

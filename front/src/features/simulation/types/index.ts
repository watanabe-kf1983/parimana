export type Eye = { text: string, type: string }

export type CandidateField = {
    name: string,
    value: number,
}
export type Candidate = {
    eye: Eye,
    odds: number,
    chance: number,
    expected: number,
    others: CandidateField[]
}

export type SimulationData = {
    eev: Array<Candidate>,
    odds_chance_chart?: string,
    odds_update_time: OddsUpdateTimeData
}
export type OddsUpdateTimeData = {
    id: string,
    description: string
}

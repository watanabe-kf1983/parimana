export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }
export type Correlation = { a: string, row: object }

export type CompetenceProps = { competences: Array<Competence>, chart: string }
export type CorrelationProps = { correlations: Array<Correlation>, chart: string }

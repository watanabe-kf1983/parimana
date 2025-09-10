export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }
export type CorrelationData = { a: string, row: object }
export type ModelData = {
    type: string,
    competences: Array<Competence>,
    competences_chart: string,
    correlations: Array<CorrelationData>,
    correlations_chart: string,
}

export const MODEL_LABELS: Record<string, string> = {
    'no_cor': 'ざっくりモデル',
    'ppf_mtx': 'ふんわりモデル',
    'bukubuku': 'ぶくぶくモデル',
    'loading': 'Loading...',
};

export const getModelLabel = (name: string) => {
    return MODEL_LABELS[name] ?? name;
};

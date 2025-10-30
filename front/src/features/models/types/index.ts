export type Competence = { contestant: string, mean: number, q1: number, q3: number, sd: number }
export type CompetencesByPlace = { place: string, competences: Array<Competence> }
export type CorrelationData = { a: string, row: object }
export type ModelData = {
    type: string,
    competences: Array<Competence>,
    competences_by_places: Array<CompetencesByPlace>,
    competences_chart: string,
    correlations: Array<CorrelationData>,
    correlations_chart: string,
}

export const MODEL_LABELS: Record<string, string> = {
    'no_cor': 'ざっくりモデル',
    'ppf_mtx': 'ふんわりモデル',
    'yurayura': 'ゆらゆらモデル',
    'combined': 'まとめ',
    'loading': 'Loading...',
};

export const PLACE_LABELS: Record<string, string> = {
    '1st': '1着あらそい',
    '2nd': '2着あらそい',
    '3rd': '3着あらそい',
};

export const getModelLabel = (name: string) => {
    return MODEL_LABELS[name] ?? name;
};

export const getPlaceLabel = (name: string) => {
    return PLACE_LABELS[name] ?? name;
};

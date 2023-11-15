import axios from "axios";

export async function getRecommendation(raceId: string, modelName: string) {
    const response = await axios.get(`http://127.0.0.1:5000/analysis/${raceId}/${modelName}`);
    return response.data;
}

export function getBoxPlotUri(raceId: string, modelName: string) {
    return `http://127.0.0.1:5000/analysis/${raceId}/${modelName}/box.png`
}

export function getOddsChartUri(raceId: string, modelName: string) {
   return  `http://127.0.0.1:5000/analysis/${raceId}/${modelName}/oc.png`
}

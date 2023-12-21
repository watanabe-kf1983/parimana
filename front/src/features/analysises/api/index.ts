import axios from "axios";
import { AnalysisStatus } from "../types";

export async function getAnalysis(raceId: string, modelName: string) {
    const response = await axios.get(`http://127.0.0.1:5000/analysis/${raceId}/${modelName}`);
    return response.data;
}

export async function getAnalysisStatus(raceId: string): Promise<AnalysisStatus> {
    const response = await axios.get(`http://127.0.0.1:5000/analyse/status/${raceId}`);
    return response.data;
}

export async function requestAnalyse(raceId: string) {
    await axios.post(`http://127.0.0.1:5000/analyse/start/${raceId}`);
}


export default { getAnalysis, getAnalysisStatus, requestAnalyse};
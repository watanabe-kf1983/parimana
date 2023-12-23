import axios from "axios";
import { AnalysisStatus } from "../types";

const hostname = window.location.hostname

export async function getAnalysis(raceId: string, modelName: string) {
    const response = await axios.get(`http://${hostname}:5000/analysis/${raceId}/${modelName}`);
    return response.data;
}

export async function getAnalysisStatus(raceId: string): Promise<AnalysisStatus> {
    const response = await axios.get(`http://${hostname}:5000/analyse/status/${raceId}`);
    return response.data;
}

export async function requestAnalyse(raceId: string) {
    await axios.post(`http://${hostname}:5000/analyse/start/${raceId}`);
}


export default { getAnalysis, getAnalysisStatus, requestAnalyse};
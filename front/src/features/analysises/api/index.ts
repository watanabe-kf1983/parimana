import axios from "axios";
import { AnalysisStatus, Candidate } from "../types";
import { EventSourceManager } from "./eventSourceManager";

const hostname = window.location.hostname
const port = API_PORT;
const baseUrl = `http://${hostname}:${port}`;


export async function getAnalysis(raceId: string, modelName: string) {
    const response = await axios.get(`${baseUrl}/analysis/${raceId}/${modelName}`);
    return response.data;
}

export async function getAnalysisStatus(raceId: string): Promise<AnalysisStatus> {
    const response = await axios.get(`${baseUrl}/analyse/status/${raceId}`);
    return response.data;
}

export async function getRecommend(raceId: string, modelName: string, query: string)
    : Promise<Array<Candidate>> {
    const response = await axios.get(`${baseUrl}/recommend/${raceId}/${modelName}/${encodeURIComponent(query)}`);
    return response.data;
}

export async function requestAnalyse(raceId: string) {
    await axios.post(`${baseUrl}/analyse/start/${raceId}`);
}

export function getProgress(raceId: string) {
    return new EventSourceManager(`${baseUrl}/analyse/progress/${raceId}`, "====END====");
}

export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress };
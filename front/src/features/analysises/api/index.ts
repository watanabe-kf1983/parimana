import axios from "axios";
import { AnalysisStatus } from "../types";
import { EventSourceManager } from "./eventSourceManager";


const hostname = window.location.hostname;
const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('<hostname>', hostname) + "/analyses";

export async function requestAnalyse(raceId: string) {
    await axios.post(`${baseUrl}/${raceId}/start`);
}

export async function getAnalysisStatus(raceId: string): Promise<AnalysisStatus> {
    const response = await axios.get(`${baseUrl}/${raceId}/status`);
    return response.data;
}

export function getProgress(raceId: string) {
    return new EventSourceManager(`${baseUrl}/${raceId}/progress`, "====END====", "====ABEND====");
}

export async function getModelList(raceId: string): Promise<string[]> {
    const response = await axios.get(`${baseUrl}/${raceId}/list`);
    return response.data;
}

export async function getAnalysis(raceId: string, modelName: string) {
    const response = await axios.get(`${baseUrl}/${raceId}/${modelName}`);
    return response.data;
}

export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress, getModelList };
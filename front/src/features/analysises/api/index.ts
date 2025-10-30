import axios from "axios";
import { AnalysisData, AnalysisStatus, ModelKey } from "../types";
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

export async function getLatestModelList(raceId: string): Promise<string[]> {
    const response = await axios.get(`${baseUrl}/${raceId}/latest/list`);
    return response.data;
}

export async function getLatestAnalysis(modelKey: ModelKey): Promise<AnalysisData> {
    const response = await axios.get(`${baseUrl}/${modelKey.raceId}/latest/${modelKey.modelName}`);
    return response.data;
}

export default { getAnalysis: getLatestAnalysis, getAnalysisStatus, requestAnalyse, getProgress, getModelList: getLatestModelList };
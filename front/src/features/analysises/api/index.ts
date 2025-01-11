import axios from "axios";
import { AnalysisStatus, Candidate } from "../types";
import { EventSourceManager } from "./eventSourceManager";

const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('${hostname}', window.location.hostname) + "/analyses";


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

export async function getAnalysis(raceId: string, modelName: string) {
    const response = await axios.get(`${baseUrl}/${raceId}/${modelName}`);
    return response.data;
}

export async function getCandidates(raceId: string, modelName: string, query: string)
    : Promise<Array<Candidate>> {
    const response = await axios.get(`${baseUrl}/${raceId}/${modelName}/candidates`, {
        params: {
            query: serverQuery(query)
        }
    });
    return response.data;
}

const serverQuery: (name: string) => string = (name) => {
    type Column = { name: string, field: string }
    const columns: Column[] = [
        { field: 'eye', name: 'Betting' },
        { field: 'type', name: 'Type' },
        { field: 'odds', name: 'Odds' },
        { field: 'chance', name: 'Chance' },
        { field: 'expected', name: 'Expectation' },
    ];
    var replacing = name;
    for (const col of columns) {
        replacing = replacing.replace(col.name, col.field)
    }
    return replacing;
}


export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress };
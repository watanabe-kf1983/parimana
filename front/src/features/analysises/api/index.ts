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

export async function getCandidates(raceId: string, modelName: string, query: string)
    : Promise<Array<Candidate>> {
    const response = await axios.get(`${baseUrl}/candidates/${raceId}/${modelName}/${encodeURIComponent(serverQuery(query))}`);
    return response.data;
}

export async function requestAnalyse(raceId: string) {
    await axios.post(`${baseUrl}/analyse/start/${raceId}`);
}

export function getProgress(raceId: string) {
    return new EventSourceManager(`${baseUrl}/analyse/progress/${raceId}`, "====END====", "====ABEND====");
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
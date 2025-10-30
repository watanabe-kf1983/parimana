import axios from "axios";
import { Candidate } from "../types";
import { ModelKey } from "../../analysises/types";


const hostname = window.location.hostname;
const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('<hostname>', hostname) + "/analyses";

export async function getCandidates(modelKey: ModelKey, timestampId: string, query: string)
    : Promise<Array<Candidate>> {
    const response = await axios.get(`${baseUrl}/${modelKey.raceId}/${timestampId}/${modelKey.modelName}/candidates`, {
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

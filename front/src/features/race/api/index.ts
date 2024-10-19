import axios from "axios";
import { Category, Race, MeetingDay, Calendar } from "../types";

const hostname = window.location.hostname
const port = API_PORT;
const baseUrl = `http://${hostname}:${port}/events/`;


export async function getCategories(): Promise<Category[]> {
    const response = await axios.get(`${baseUrl}/categories`);
    return response.data;
}

export async function getCalendar(categoryId: string): Promise<Calendar> {
    const response = await axios.get(`${baseUrl}/calendar`, {
        params: {
            category: categoryId
        }
    });
    return response.data;
}

export async function getRaces(md: MeetingDay): Promise<Race[]> {
    const response = await axios.get(`${baseUrl}/races`, {
        params: {
            category: md.category.id,
            course: md.course.id,
            date: md.date
        }
    });
    return response.data;
}

export async function findRaceByUri(uri: String): Promise<Race | undefined> {
    const response = await axios.get(`${baseUrl}/races`, {
        params: {
            uri: uri,
        }
    });
    return response.data;
}

export async function getRace(raceId: string): Promise<Race> {
    const response = await axios.get(`${baseUrl}/races/${raceId}`);
    return response.data;
}


// export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress };
import axios from "axios";
import { Category, RaceInfo, Calendar } from "../types";

const hostname = window.location.hostname;
const port = API_PORT;
const baseUrl = `http://${hostname}:${port}/events`;

export async function getCategories(): Promise<Category[]> {
  const response = await axios.get(`${baseUrl}/categories`);
  return response.data;
}

export async function getCalendar(categoryId: string): Promise<Calendar> {
  const response = await axios.get(`${baseUrl}/calendars/${categoryId}`);
  return response.data;
}

export async function findRaceByUri(
  uri: String
): Promise<RaceInfo | undefined> {
  const response = await axios.get(`${baseUrl}/races`, {
    params: {
      uri: uri,
    },
  });
  return response.data;
}

export async function getRaceInfo(raceId: string): Promise<RaceInfo> {
  const response = await axios.get(`${baseUrl}/races/${raceId}`);
  return response.data;
}

// export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress };

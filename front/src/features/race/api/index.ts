import axios from "axios";
import Axios from "axios";
import { Category, RaceInfo } from "../types";

const hostname = window.location.hostname;
const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('<hostname>', hostname);

export async function getCategories(): Promise<Category[]> {
  const response = await axios.get(`${baseUrl}/schedule/categories`);
  return response.data;
}

export async function getCalendar(categoryId: string, analysedOnly: boolean): Promise<RaceInfo[]> {
  const response = await axios.get(`${baseUrl}/schedule/races`, {
    params: {
      category_id: categoryId,
      analysed_only: analysedOnly
    },
  });
  return response.data;
}

export async function getRaceInfo(raceId: string): Promise<RaceInfo> {
  try {
    const response = await axios.get(`${baseUrl}/schedule/races/${raceId}`);
    return response.data;
  } catch (e) {
    if (Axios.isAxiosError(e) && e.response && e.response.status === 404) {
      throw new NotFoundError(`raceinfo of ${raceId} not found`);
    } else {
      throw e;
    }
  }
}

export class NotFoundError extends Error {
  public constructor(message?: string) {
    super(message);
  }
}

export async function postRaceInfo(raceId: string): Promise<RaceInfo> {
  const response = await axios.post(`${baseUrl}/schedule/races/${raceId}`);
  return response.data;
}

export async function findRaceIdByUri(uri: string): Promise<string> {
  const params = new URLSearchParams()
  params.append("url", uri)
  const response = await axios.get(`${baseUrl}/analyses/race_id`, { params: params });
  return response.data;
}

// export default { getAnalysis, getAnalysisStatus, requestAnalyse, getProgress };

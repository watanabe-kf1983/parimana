import axios from "axios";
import { Category, RaceInfo } from "../types";

const hostname = window.location.hostname;
const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('<hostname>', hostname) + "/schedule";

export async function getCategories(): Promise<Category[]> {
  const response = await axios.get(`${baseUrl}/categories`);
  return response.data;
}

export async function getCalendar(categoryId: string, analysedOnly: boolean): Promise<RaceInfo[]> {
  const response = await axios.get(`${baseUrl}/races`, {
    params: {
      category_id: categoryId,
      analysed_only: analysedOnly
    },
  });
  return response.data;
}

export async function findRaceByUri(
  uri: String
): Promise<RaceInfo | undefined> {
  const response = await axios.get(`${baseUrl}/races/`, {
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

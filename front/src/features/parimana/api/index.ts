import axios from "axios";
import { AppInfo } from "../types";

const hostname = window.location.hostname;
const baseUrl = import.meta.env.VITE_API_URL_BASE.replace('<hostname>', hostname);

export async function getAppInfo(): Promise<AppInfo> {
    const response = await axios.get(`${baseUrl}/info`);
    return response.data;
}

export default { getAppInfo };
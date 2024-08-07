import createClient from "openapi-fetch";
import {paths} from "@/lib/backend/type";


export const createBackendClient = () => {
    return createClient<paths>({ baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL! })
}
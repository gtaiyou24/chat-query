export const BASE_URL = process.env.NODE_ENV === "production"
    ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}` ?? 'https://analyticsgpt.com'
    : 'http://localhost:3000';

export const APP_NAME = 'Analytics GPT';
export const X_CREATOR = '@tm_taiyo';
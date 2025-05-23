import dotenv from "dotenv";

dotenv.config();

export const PORT = process.env.PORT || 3000;
export const OPENAI_API_KEY = process.env.OPENAI_API_KEY!;

export const TRANSCRIPTS_BUCKET_NAME = "pcp-transcripts";
export const EPISODES_BUCKET_NAME = "pcp-episodes";

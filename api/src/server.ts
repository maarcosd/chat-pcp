import { Storage } from "@google-cloud/storage";
import cors from "cors";
import express from "express";
import { agent } from "./agents";
import { EPISODES_BUCKET_NAME, PORT } from "./config";
import { Episode } from "./types";

const app = express();
const storage = new Storage();
const bucket = storage.bucket(EPISODES_BUCKET_NAME);

app.use(cors());
app.use(express.json());

// Routes
app.get("/api/episodes", async (_, res) => {
  try {
    const [files] = await bucket.getFiles({
      maxResults: 1000,
      autoPaginate: false,
    });
    const episodes: Episode[] = [];

    for (const file of files) {
      if (file.name.endsWith(".json")) {
        const [content] = await file.download();
        const episode: Episode = JSON.parse(content.toString());
        episodes.push(episode);
      }
    }

    res.json({ episodes: episodes.reverse() });
  } catch (error) {
    console.error("Error reading episodes:", error);
    res.status(500).json({ error: "Failed to fetch episodes" });
  }
});

// AI Chat endpoint
app.post("/api/chat", async (req, res) => {
  try {
    const { messages } = req.body;

    // Set up the response headers for streaming
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");

    // Transform the stream and send chunks to the response
    for await (const chunk of agent.processMessages(messages)) {
      res.write(chunk);
    }

    res.end();
  } catch (error) {
    console.error("Error in chat:", error);
    res.status(500).json({ error: "Chat processing failed" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});

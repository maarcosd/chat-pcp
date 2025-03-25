import { Storage } from "@google-cloud/storage";
import cors from "cors";
import express from "express";
import { agent } from "./agents";
import { EPISODES_BUCKET_NAME, PORT } from "./config";

const app = express();
const storage = new Storage();
const bucket = storage.bucket(EPISODES_BUCKET_NAME);

app.use(cors());
app.use(express.json());

// Routes
app.get("/api/episodes", async (req, res) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const pageSize = parseInt(req.query.pageSize as string) || 10;
    const searchQuery = ((req.query.search as string) || "").toLowerCase();

    if (page < 1 || pageSize < 1) {
      return res
        .status(400)
        .json({ error: "Page and pageSize must be positive numbers" });
    }

    const [files] = await bucket.getFiles({
      maxResults: 1000,
      autoPaginate: false,
    });

    // Create array of file metadata and names
    const fileInfos = files
      .filter((file) => file.name.endsWith(".json"))
      .map((file) => ({
        name: file.name,
        creationTime: file.metadata.timeCreated!,
      }))
      .sort(
        (a, b) =>
          new Date(b.creationTime).getTime() -
          new Date(a.creationTime).getTime()
      );

    // Filter files based on search query if provided
    const filteredFileInfos = searchQuery
      ? fileInfos.filter((fileInfo) => {
          // Replace hyphens with spaces in filename for comparison
          const normalizedFilename = fileInfo.name.replace(/-/g, " ");
          return normalizedFilename.toLowerCase().includes(searchQuery);
        })
      : fileInfos;

    // Calculate pagination after filtering
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedFileInfos = filteredFileInfos.slice(startIndex, endIndex);

    // Download only the filtered and paginated files
    const episodes = await Promise.all(
      paginatedFileInfos.map(async (fileInfo) => {
        const file = bucket.file(fileInfo.name);
        const [content] = await file.download();
        return JSON.parse(content.toString());
      })
    );

    res.json({
      episodes,
      pagination: {
        currentPage: page,
        pageSize,
        totalEpisodes: filteredFileInfos.length,
        totalPages: Math.ceil(filteredFileInfos.length / pageSize),
      },
    });
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

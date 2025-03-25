import { Chroma } from "@langchain/community/vectorstores/chroma";
import { Document } from "@langchain/core/documents";
import { tool } from "@langchain/core/tools";
import { OpenAIEmbeddings } from "@langchain/openai";
import { z } from "zod";

const toolParams = {
  name: "query_rag",
  description: "Fetch relevant from the podcast transcripts",
  schema: z.object({
    queryText: z.string().describe("The question being asked"),
  }),
};

export const queryRag = tool(
  async ({ queryText }): Promise<{ context: string; sources: string[] }> => {
    console.log("Starting queryRag with query:", queryText);

    try {
      const embeddingFunction = new OpenAIEmbeddings();
      const db = await Chroma.fromExistingCollection(embeddingFunction, {
        collectionName: "transcripts",
        url: "http://localhost:8000", // ChromaDB server URL
      });

      const results = await db.similaritySearchWithScore(queryText, 100, {
        date: { $ne: "" }, // This is a hack to get around a bug in ChromaDB
      });

      // Check if there are any matching results or if relevance score is too low
      if (results.length === 0) {
        return {
          context:
            "I couldn't find any relevant information in the podcast transcripts.",
          sources: [],
        };
      }

      // Combine context from matching documents
      const contextText = results
        .map(([doc, _]: [Document, number]) => {
          return doc.pageContent;
        })
        .join("\n\n - -\n\n");

      // Get sources
      const sources = [
        ...new Set(
          results.map(
            ([doc, _score]: [Document, number]) => doc.metadata?.title || null
          )
        ),
      ].filter(Boolean);

      return { context: contextText, sources };
    } catch (error) {
      console.error("Error in queryRag:", error);
      throw error;
    }
  },
  toolParams
);

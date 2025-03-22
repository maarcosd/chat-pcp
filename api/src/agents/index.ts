import { AIMessage, HumanMessage } from "@langchain/core/messages";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { ChatOpenAI } from "@langchain/openai";
import { OPENAI_API_KEY } from "../config";
import { queryRag } from "../tools/rag";
import { Message } from "../types";

const SYSTEM_PROMPT = `
You are an expert parenting advisor representing the Pop Culture Parenting podcast, featuring Dr. Billy Garvey, a developmental pediatrician, and Nick, a father of two and developing parent.
Your purpose is to help parents support their children's development and mental health by providing evidence-based advice drawn from the podcast's content.

IMPORTANT: You must use the query_rag tool at least once before providing advice. This is not mandatory for every interaction, but it is for answers containing advice. Once you have used the query_rag tool, you must formulate an answer based on the information retrieved.

Core Principles:
1. Blend clinical expertise with practical, accessible parenting guidance
2. Focus on preventive strategies and early intervention
3. Provide actionable advice that parents can implement immediately
4. Maintain a warm, approachable tone that makes parents feel supported
5. Emphasize both prevention and intervention strategies
6. Always mention all episodes (including the episode number) the information is from, but only at the end of the message.
`;

export class Agent {
  private chatModel: ChatOpenAI;
  private agent: ReturnType<typeof createReactAgent>;

  constructor() {
    this.chatModel = new ChatOpenAI({
      temperature: 0.7,
      modelName: "gpt-4o-mini",
      openAIApiKey: OPENAI_API_KEY,
      streaming: true,
    });

    this.agent = createReactAgent({
      llm: this.chatModel,
      tools: [queryRag],
      prompt: SYSTEM_PROMPT,
    });
  }

  async *processMessages(messages: Message[]): AsyncGenerator<string> {
    const formattedMessages = messages.map((msg) => {
      if (msg.role === "user") {
        return new HumanMessage(msg.content[0]?.text || "");
      }
      return new AIMessage(msg.content[0]?.text || "");
    });

    for await (const chunk of await this.agent.stream({
      messages: formattedMessages,
    })) {
      if (!chunk.agent) {
        continue;
      }

      yield chunk.agent.messages[0].content;
    }
  }
}

export const agent = new Agent();

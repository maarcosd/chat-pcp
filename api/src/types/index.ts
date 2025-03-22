export interface Episode {
  title: string;
  summary: string;
  pub_date: string;
  link: string;
  audio_url: string;
  keywords: string[];
}

export interface Message {
  role: "user" | "assistant";
  content: [{ type: string; text: string }];
}

export interface AgentConfig {
  modelName: string;
  temperature: number;
  streaming: boolean;
  apiKey: string;
}

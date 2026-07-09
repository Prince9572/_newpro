// import { config } from "dotenv";
// config();

// import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
// import { AgentExecutor, createReactAgent } from "langchain/agents";
// import { SerpAPI } from "@langchain/community/tools/serpapi";
// import { pull } from "langchain/hub";
import { config } from "dotenv";
config();

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { SerpAPI } from "@langchain/community/tools/serpapi";
import { PromptTemplate } from "@langchain/core/prompts";

// CHANGE THESE TWO: Import from the main 'langchain' entry point, 
// OR directly from the specific sub-packages.
//import { AgentExecutor, createReactAgent } from "langchain/agents";
import { AgentExecutor } from "langchain/agents";
import { createReactAgent } from "langchain/agents";

const model = new ChatGoogleGenerativeAI({
    modelName: "gemini-1.5-flash", 
    maxOutputTokens: 2048,
    temperature: 0.7,
    apiKey: process.env.GOOGLE_API_KEY,
});

// Define the tool
const searchTool = new SerpAPI(process.env.SERPAPI_API_KEY, {
    location: "India",
});

const tools = [searchTool];

// Pull a standard ReAct prompt from the LangChain Hub
const prompt = await pull("hwchase17/react");

// Initialize the Agent
const agent = await createReactAgent({
    llm: model,
    tools,
    prompt,
});

// Create the Executor
const executor = new AgentExecutor({
    agent,
    tools,
});

// Invoke the agent
const res = await executor.invoke({
    input: "What is the latest news about AI?",
});

console.log("Final output:", res.output);
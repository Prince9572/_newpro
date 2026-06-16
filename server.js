import express from "express";
import dotenv from "dotenv";
import path from "path";

import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { DynamicStructuredTool } from "@langchain/core/tools";
import {
  ChatPromptTemplate,
  MessagesPlaceholder,
} from "@langchain/core/prompts";

import {
  AgentExecutor,
  createToolCallingAgent,
} from "langchain/agents";

import { z } from "zod";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const __dirname = path.resolve();


// ======================================================
// GEMINI MODEL
// ======================================================

const model = new ChatGoogleGenerativeAI({
  model: "models/gemini-2.5-flash",
  temperature: 0.7,
  maxOutputTokens: 2048,
  apiKey: process.env.GOOGLE_API_KEY,
});


// ======================================================
// MENU DATABASE
// ======================================================

const menus = {
  italian: {
    breakfast: [
      "Croissant",
      "Cappuccino",
      "Frittata",
      "Bruschetta",
      "Cornetto",
      "Ricotta Pancakes",
    ],
    lunch: [
      "Margherita Pizza",
      "Lasagna",
      "Risotto",
      "Pasta Alfredo",
      "Minestrone Soup",
      "Caprese Salad",
    ],
    dinner: [
      "Spaghetti Carbonara",
      "Chicken Parmesan",
      "Seafood Risotto",
      "Truffle Pasta",
      "Osso Buco",
      "Tiramisu",
    ],
  },

  american: {
    breakfast: [
      "Pancakes",
      "Scrambled Eggs",
      "Bacon",
      "Hash Browns",
      "French Toast",
    ],
    lunch: [
      "Cheeseburger",
      "BBQ Wings",
      "Hot Dog",
      "Mac and Cheese",
      "Club Sandwich",
    ],
    dinner: [
      "Steak",
      "BBQ Ribs",
      "Burger with Fries",
      "Fried Chicken",
      "Apple Pie",
    ],
  },

  indian: {
    breakfast: [
      "Aloo Paratha",
      "Poha",
      "Dosa",
      "Idli Sambar",
      "Chole Bhature",
    ],
    lunch: [
      "Butter Chicken",
      "Dal Tadka",
      "Biryani",
      "Rajma Chawal",
      "Paneer Butter Masala",
    ],
    dinner: [
      "Tandoori Chicken",
      "Rogan Josh",
      "Malai Kofta",
      "Fish Curry",
      "Gulab Jamun",
    ],
  },

  chinese: {
    breakfast: [
      "Bao Buns",
      "Congee",
      "Dumplings",
      "Scallion Pancakes",
    ],
    lunch: [
      "Kung Pao Chicken",
      "Fried Rice",
      "Chow Mein",
      "Dim Sum",
    ],
    dinner: [
      "Peking Duck",
      "Mapo Tofu",
      "Szechuan Chicken",
      "Beef Noodles",
    ],
  },

  mexican: {
    breakfast: [
      "Huevos Rancheros",
      "Breakfast Burrito",
      "Churros",
    ],
    lunch: [
      "Tacos",
      "Nachos",
      "Burrito Bowl",
      "Chicken Enchiladas",
    ],
    dinner: [
      "Fajitas",
      "Quesabirria",
      "Chili Con Carne",
      "Tres Leches Cake",
    ],
  },

  japanese: {
    breakfast: [
      "Miso Soup",
      "Rice Balls",
      "Tamago Sushi",
    ],
    lunch: [
      "Ramen",
      "Sushi",
      "Tempura",
      "Chicken Katsu",
    ],
    dinner: [
      "Yakitori",
      "Shabu Shabu",
      "Sashimi",
      "Okonomiyaki",
    ],
  },

  french: {
    breakfast: [
      "Croissant",
      "Cafe au Lait",
      "Crepes",
    ],
    lunch: [
      "French Onion Soup",
      "Quiche Lorraine",
      "Croque Monsieur",
    ],
    dinner: [
      "Coq au Vin",
      "Duck Confit",
      "Creme Brulee",
    ],
  },
};


// ======================================================
// HELPERS
// ======================================================

const cuisineTypes = Object.keys(menus);

const mealTypes = [
  "breakfast",
  "lunch",
  "dinner",
];

const capitalize = (text = "") =>
  text.charAt(0).toUpperCase() + text.slice(1);

const detectCuisine = (text = "") => {
  const lower = text.toLowerCase();

  return cuisineTypes.find((cuisine) =>
    lower.includes(cuisine)
  );
};

const detectMealType = (text = "") => {
  const lower = text.toLowerCase();

  return mealTypes.find((meal) =>
    lower.includes(meal)
  );
};


// ======================================================
// MENU TOOL
// ======================================================

const getMenuTool = new DynamicStructuredTool({
  name: "getMenuTool",

  description:
    "Get restaurant menu items using cuisine and mealType.",

  schema: z.object({
    cuisine: z.string().optional(),
    mealType: z.string().optional(),
  }),

  func: async ({ cuisine, mealType }) => {

    if (!cuisine && !mealType) {
      return `
Available cuisines:
${cuisineTypes.join(", ")}

Available meal types:
${mealTypes.join(", ")}
      `;
    }

    if (cuisine && !menus[cuisine]) {
      return `
Cuisine not found.

Available cuisines:
${cuisineTypes.join(", ")}
      `;
    }

    // Cuisine + Meal Type
    if (cuisine && mealType) {

      const items = menus[cuisine][mealType];

      if (!items) {
        return `Meal type not found for ${cuisine}.`;
      }

      return `
🍽 ${capitalize(cuisine)} ${capitalize(mealType)} Menu

${items.map((item, index) => `${index + 1}. ${item}`).join("\n")}
      `;
    }

    // Only Cuisine
    if (cuisine) {

      const menu = menus[cuisine];

      return `
🍴 ${capitalize(cuisine)} Full Menu

🌅 Breakfast:
${menu.breakfast.map((item) => `• ${item}`).join("\n")}

☀️ Lunch:
${menu.lunch.map((item) => `• ${item}`).join("\n")}

🌙 Dinner:
${menu.dinner.map((item) => `• ${item}`).join("\n")}
      `;
    }

    // Only Meal Type
    if (mealType) {

      let result = `🍽 ${capitalize(mealType)} Specials\n\n`;

      cuisineTypes.forEach((cuisine) => {
        result += `🍴 ${capitalize(cuisine)}:\n`;
        result += menus[cuisine][mealType]
          .map((item) => `• ${item}`)
          .join("\n");

        result += "\n\n";
      });

      return result;
    }

    return "No menu found.";
  },
});


// ======================================================
// PROMPT
// ======================================================

const prompt = ChatPromptTemplate.fromMessages([
  [
    "system",
    `
You are a smart restaurant AI assistant.

Your job:
- Help users with restaurant menus
- Recommend foods
- Suggest cuisines
- Answer naturally like a real restaurant assistant
- Keep responses clean and human-like
- Use tools whenever menu information is required
`,
  ],

  ["human", "{input}"],

  new MessagesPlaceholder("agent_scratchpad"),
]);


// ======================================================
// AGENT
// ======================================================

const agent = await createToolCallingAgent({
  llm: model,
  tools: [getMenuTool],
  prompt,
});

const executor = new AgentExecutor({
  agent,
  tools: [getMenuTool],
  verbose: true,
  maxIterations: 3,
});


// ======================================================
// FRONTEND ROUTE
// ======================================================

app.get("/", (req, res) => {
  res.sendFile(
    path.join(__dirname, "public", "index.html")
  );
});


// ======================================================
// CHAT API
// ======================================================

app.post("/api/chat", async (req, res) => {

  try {

    const input = req.body.input?.trim();

    if (!input) {
      return res.status(400).json({
        output: "Please enter a message.",
      });
    }

    console.log("User:", input);

    // Fast menu detection
    const cuisine = detectCuisine(input);
    const mealType = detectMealType(input);

    // Direct Tool Call
    if (cuisine || mealType) {

      const result = await getMenuTool.invoke({
        cuisine,
        mealType,
      });

      return res.json({
        output: result,
      });
    }

    // AI Agent
    const response = await executor.invoke({
      input,
    });

    return res.json({
      output: response.output,
    });

  } catch (error) {

    console.error("ERROR:", error);

    return res.status(500).json({
      output:
        "Sorry, something went wrong. Please try again.",
    });
  }
});


// ======================================================
// SERVER
// ======================================================

app.listen(PORT, () => {
  console.log(`
🍽 Restaurant AI Server Running
🌐 http://localhost:${PORT}
  `);
});
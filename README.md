# LLM-Powered Research Agent

This project presents a sophisticated research agent designed to automate the process of gathering, summarizing, and reporting information from the web. What makes this project truly stand out is its innovative approach to leveraging local Large Language Models (LLMs) powered by Ollama. This design choice ensures enhanced data privacy, reduces reliance on external API costs for core reasoning and summarization tasks, and provides a robust, self-contained environment for your research needs.

The agent intelligently generates search queries, scrapes relevant web content, summarizes key information, and compiles a comprehensive final report, all orchestrated through a well-defined workflow. This project truly showcases the power and flexibility of running advanced AI models right on your machine!

---

## Features

* **Intelligent Query Generation**: Dynamically creates effective search queries based on your research prompt.
* **Robust Web Scraping**: Utilizes both simple HTTP requests and Playwright for handling dynamic, JavaScript-heavy websites.
* **Contextual Summarization**: Summarizes scraped web content, focusing on relevance to the original query.
* **Comprehensive Report Generation**: Compiles all gathered and summarized information into a detailed, coherent report.
* **Local LLM Integration**: Powered by Ollama, enabling you to run powerful LLMs locally on your machine for privacy, cost efficiency, and full control over your AI environment.

---

## Getting Started

Follow these clear instructions to set up and run the LLM-Powered Research Agent.

---

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **pip** (Python package installer)
* **Ollama** (for running local LLMs)

---

### Step 1: Project Setup

Make sure all your project files (agent.py, brave_search.py, final_response.py, query_maker.py, re_extraction.py, search_data.py, summarizer.py) are in the same directory.

---

### Step 2: Install Python Dependencies

Navigate to your project directory in the terminal and install the required Python libraries:

`pip install langchain-ollama langchain-core requests python-dotenv inscriptis playwright`

`playwright install` # Install browser binaries for Playwright

---

### Step 3: Set up Ollama and Download Models

This project is built to leverage the power of local Large Language Models using Ollama.

#### Download and Install Ollama:

If you don't have Ollama installed, download it from the official website: https://ollama.com/
For a detailed guide on setting up Ollama and managing models, refer to this excellent article: https://basitsameerpersonalportfolio.vercel.app/blogs/ollama-your-local-gateway-to-large-language-models

#### Download the Required LLM Models:

Your agent uses the following specific models from Ollama for its operations:

* **qwen3:8b** (primarily for generating the final comprehensive research report)
* **qwen2.5:1.5b** (used for generating concise search queries and summarizing website content)

Open your terminal and run the following commands to download these models:

`ollama pull qwen3:8b`
`ollama pull qwen2.5:1.5b`

**Important**: Ensure Ollama is running in the background (as a service or in a separate terminal window) while you use the agent, as it needs to connect to the local Ollama server to access these models.

---

### Step 4: Obtain a Brave Search API Key

The agent uses the Brave Search API to perform its initial web searches.

#### Sign Up:

Visit the Brave Search API website (a quick search for "Brave Search API" will lead you there).

#### Get Your API Key:

After signing up and logging in, you should be able to generate or find your unique X-Subscription-Token.

#### Create a .env file:

In the root directory of your project, create a new file named `.env` and add your Brave API key to it like this:

`Brave_API="YOUR_BRAVE_API_KEY_HERE"`

Remember to replace "YOUR_BRAVE_API_KEY_HERE" with the actual key you obtained. This file keeps your sensitive key out of your main code and version control.

---

### Step 5: Run the Agent

You have two convenient ways to run the agent: via the command line for direct interaction.

#### Option 1: Command Line Interface (CLI)

This option runs the agent directly from its core agent.py file. It will prompt you for input and display progress and the final report in your terminal.

`python agent.py`

The agent will welcome you and then ask for your research prompt.
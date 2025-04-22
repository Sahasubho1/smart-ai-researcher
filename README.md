# AI Summarizer using Langchain and Google Gemini

This project uses Langchain, Tavily, and Google Gemini APIs to create an intelligent summarizer that answers questions based on the latest news and information available on the web.

## Overview

The application retrieves the latest relevant news and content using the Tavily API based on a user query, then summarizes it using the ChatGoogleGenerativeAI model powered by Google Gemini.

## Key Components

- **Tavily API**: Used to search and fetch the latest content based on a given query.
- **Google Gemini API**: Used to summarize the fetched content and generate answers to the user's query.
- **Langchain**: A framework that integrates various language models and tools to create sophisticated pipelines.
- **Langgraph**: Used for managing the flow of the pipeline, from fetching content to generating a summary.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_name>

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


from tavily import TavilyClient
from typing import TypedDict

from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

load_dotenv()

tavily_api_key = os.getenv("api_key")
gemini_api_key = os.getenv("gemini_api")

class AppState(TypedDict):
    query: str
    context: str
    result: str

def researcher(state):
    query = state["query"]
    client = TavilyClient(api_key=tavily_api_key)
    
    response = client.search(
    query,
    search_depth="basic",
    time_range="week",
    include_raw_content=True,
    max_results=5,
    topic="general"
    )
    context = "\n\n".join(
    result.get("raw_content", "") for result in response.get("results", []) if result.get("raw_content")
    )

    state["context"] = context

    return state

def summarization(state):
    query = state["query"]
    context = state["context"]

    model = ChatGoogleGenerativeAI(api_key=gemini_api_key, 
                                   model="gemini-1.5-pro",
                                   temperature = 0.7)

    prompt = PromptTemplate(
    input_variables=["context", "query"],
    template="""
    You are a helpful and concise summarizer agent. Answer the question using only the relevant information provided in the context. 
    Avoid adding any information that is not grounded in the context.
    
    Context:
    {context}
    
    Question:
    {query}
    
    Answer:"""
    )

    chain = LLMChain(llm=model, prompt=prompt)

    result = chain.invoke({"context": context, "query": query})

    state["result"] = result["text"]

    return state

graph= StateGraph(AppState)
graph.add_node("search" , researcher)
graph.add_node("summarizer", summarization)
graph.set_entry_point("search")
graph.add_edge("search", "summarizer")
graph.add_edge("summarizer", END)
app = graph.compile()

if __name__ == "__main__":
    query = input("Enter query: ")
    output = app.invoke({"query" : query})
    print("Summarized Result: ")
    print(output["result"])

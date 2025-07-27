from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def query_maker(prompt):
    template = """
    You are a search query generator.

    You will be given a user prompt. Your job is to return a list of search queries relevant to that prompt.

    REQUIREMENTS:
    - Output ONLY a list of 5 to 7 search queries in Python list format.
    - Make the queries consice and accurate not long queries
    - DO NOT include explanations, comments, greetings, or anything else.
    - Format: ["query 1", "query 2", ..., "query n"]

    EXAMPLE:
    [USER_PROMPT]: How to learn to build agents
    [Your Answer]: ["build AI agents", "LLM agent tutorial", "LangChain agents", "Python agent frameworks", "agentic AI examples"]

    NOW GENERATE SEARCH QUERIES FOR:
    [USER_PROMPT]: {prompt}
    [Your Answer]:
"""
    cp = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model='qwen2.5:1.5b')
    
    chain = cp | model
    Queries = chain.invoke({"prompt":prompt})
    return Queries

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def website_sumarizer(i,url,query,data):
    template = """
    As a highly skilled text summarizer, your task is to synthesize information from the provided web content.

    **Instructions:**
    1.  **Focus on Relevance:** Prioritize information directly related to the user's search query: **"{query}"**.
    2.  **Filter Irrelevant Content:** Disregard common web page boilerplate, such as navigation menus, footers, advertisements, sidebars, or any other elements not central to the main article or informational body of the page.
    3.  **Maintain Key Information:** Ensure that all critical details, facts, and conclusions from the relevant content are retained in the summary. Do not omit any significant information.
    4.  **Contextual Reference:** The original content was sourced from this URL: {url}. Use this for context, but do not include the URL in the summary itself.

    **Original Web Content:**
    {content}

    **Summary:**
    """

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model='qwen2.5:1.5b')
    chain = prompt | model

    summarize_text = chain.invoke({"content": data,'url':url,"query":query})
    print(f"[✅] Summarization of {i} website Completed")
    return summarize_text


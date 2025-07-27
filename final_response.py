from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def make_final_response(query,data):
    template = """
    You are an expert analyst and report writer. You will be given scraped data from many websites. The data was scrapped based on this input from the user {query}. 
    then That query was used to generate search terms to serach the web.
    Produce a high‑quality, comprehensive, and coherent report of at least 1000 words.
    Here is the data, Websites data: {data}.
    
    Instructions:
    - Write a **detailed report** based on this data and include anything neccessary according to you.
    - Cover key themes, insights, structure logically (e.g. Introduction, Details, Implications, Conclusion).
    - Use clear headings.
    - Maintain objective and professional tone.
    - Ensure the final report is **at least 1000 words**.

    Begin your report below:
    """

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model='qwen3:8b')
    chain = prompt | model

    summarize_text = chain.invoke({"data": data,'query':query})
    return summarize_text


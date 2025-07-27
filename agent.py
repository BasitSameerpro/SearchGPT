from langgraph.graph import StateGraph,START,END
from brave_search import Brave_SERP
from search_data import data
# from re_extraction import etuData
from summarizer import website_sumarizer
from query_maker import query_maker
from final_response import make_final_response
import json,ast
from typing import TypedDict
import asyncio

class State(TypedDict):
    prompt: str
    search_queries: list
    url_lists : list
    scrapped_data: list
    summaries : list
    final_response : str
    
class llm_agent:
    def __init__(self):
        self.prompt = None
        self.final_response = None
        self.queries : list = None
        self.graph = None
    
    def get_user_prompt(self,state: State) -> State:
        print("Welcome to searchGPT 😊😊😊")
        print("What would you like to research today")
        self.prompt = input("Lets HitchHike. User: ")
        state['prompt'] = self.prompt   
        return state
    
    def get_search_queries(self, state: State) -> State:
        max_attempts = 5
        print("→ Tring to get queries from llm")
        for _ in range(max_attempts):
            raw = query_maker(state['prompt'])

            # 1) If it's already a list, we’re done:
            if isinstance(raw, list):
                queries = raw

            # 2) Otherwise try JSON parse:
            else:
                try:
                    queries = json.loads(raw)
                except json.JSONDecodeError:
                    # 3) Fallback to safe Python literal eval:
                    try:
                        queries = ast.literal_eval(raw)
                    except (ValueError, SyntaxError):
                        queries = None

            # 4) Check we got a list:
            if isinstance(queries, list):
                self.queries = queries
                state['search_queries'] = queries
                break
        else:
            raise ValueError("query_maker did not return a list after 5 attempts.")
        print(f"✓ Got queries to search for {state['search_queries']}")
        return state
        
    def get_SERP(self,state:State)-> State:
        url_links = []
        print("§ Trying to get url links")
        for query in state['search_queries']:
            link = Brave_SERP(query)
            url_links.append(link)
            
        url_links_data = [item for sublist in url_links for item in sublist] # This is to make a list of dicts
        url_links = [l['url'] for l in url_links_data] # To get url from list of dicts
        unique_links = list(set(url_links)) # to remove duplicate links
         # filter out any PDF links
        filtered_links = [
            url for url in unique_links
            if not url.lower().rstrip('/').endswith('.pdf')
        ]
        state['url_lists'] = filtered_links
        print("✓ Completed getting urls")
        return state
    
    async def get_data_from_websites(self,state: State)->State:
        print("→ Scrapping data from websites")
        links = state['url_lists']
        all_data = []
        d = data()
        for i,link in enumerate(links,1):
            website_data = await d.run(link)
            w_data = {
                'Link Number' : i,
                'Website Url' : link,
                'Website Data': website_data
            }
            all_data.append(w_data)
            
        state['scrapped_data'] = all_data
        print("✓ Scrapping completed")
        return state
    
    def _get_data_sync(self, state):
        return asyncio.run(self.get_data_from_websites(state))

    def summarize_website_data(self,state:State)->State:
        print("! Getting summaries of the websites. This may take a while ")
        data_to_summarize = state['scrapped_data']
        queries = self.queries # Now i have to decide that fo 5 iter one query then next 5 next query and so on
        summarized_data = []
        for i,data in enumerate(data_to_summarize):
            url = data['Website Url']
            website_data = data['Website Data']
            query_index = (i // 5) % len(queries)
            query = queries[query_index]
            llm_summary = website_sumarizer(i,url,query,website_data)
            summary = {
                "Website Url": url,
                "Website Summary" : llm_summary
            }
            summarized_data.append(summary)
            
        state['summaries'] = summarized_data
        print("✓ Summarization Completed")
        return state
    
    def get_final_response(self,state: State)->State:
        print("😊😊 Compiling the final response")
        data = str(state['summaries'])
        try: 
            final_response = make_final_response(self.prompt , data)
            state['final_response'] = final_response
            print(state['final_response'])
        except Exception as e:
            print(f"[ERROR OCCURED]: {e} ")

        return state
    
    def workflow(self):
        
        graphbuilder = StateGraph(State)
        
        # Add nodes
        graphbuilder.add_node("user_prompt", self.get_user_prompt)
        graphbuilder.add_node("search_query", self.get_search_queries)
        graphbuilder.add_node('SERP', self.get_SERP)
        graphbuilder.add_node('website_data',self._get_data_sync)
        graphbuilder.add_node('summarize_website_data',self.summarize_website_data)
        graphbuilder.add_node('make_final_response',self.get_final_response)
        
        # Add edges
        graphbuilder.add_edge(START,'user_prompt')
        graphbuilder.add_edge('user_prompt','search_query')
        graphbuilder.add_edge('search_query','SERP')
        graphbuilder.add_edge('SERP','website_data')
        graphbuilder.add_edge('website_data','summarize_website_data')
        graphbuilder.add_edge('summarize_website_data','make_final_response')
        graphbuilder.add_edge('make_final_response',END)
        
        # Compile graph
        self.graph = graphbuilder.compile()
        
    def run(self):
        if self.graph is None:
            self.workflow()
            
        state: State = {}
        self.graph.invoke(state)
        
llm = llm_agent()
llm.run()

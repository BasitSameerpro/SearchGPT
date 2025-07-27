import os
import re

class etuData:
    def make_chunks(self,data , characters=500):
        data_chunks = []
        for i in range(0 , len(data) , characters):
            chunk = data[i:i+characters]
            data_chunks.append(chunk)
        return data_chunks
    
    def useRE(self,query,data_chunks):
        query_words = query.split()
        # Match full phrase OR individual words
        full_phrase = re.escape(query)
        word_pattern = r'\b(?:' + '|'.join(re.escape(word) for word in query_words) + r')\b'
        pattern = r'(?:' + full_phrase + r'|' + word_pattern + r')'
        
        relevant_chunks = []
        for i, chunk in enumerate(data_chunks, 1):
            if re.search(pattern, chunk, re.IGNORECASE):
                relevant_chunks.append(chunk)
        
        return relevant_chunks  
        
    def extract(self,data,query,character=0):
        if character <= 0:
            character = 500
        chunks = self.make_chunks(data,character)
        match_data = self.useRE(query,chunks)
        return match_data
        
e = etuData()
data = e.extract(data,'llm agents')
data = print(data)

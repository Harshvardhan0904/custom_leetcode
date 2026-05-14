import json
import os 
from llm.get_ai_tags import valid_tags
file_name = "llm_cache.json"

def load_cache(file_name=file_name):
    if os.path.exists(file_name):
        with open(file_name,'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(file_name,'w') as f:
        json.dump(cache,f,indent=2)

def get_tags_from_domain(domain:str):
    cache = load_cache()
    if domain in cache:
        print("[DOMAIN PRESENT IN CACHE]")
        return cache[domain]
    
    tags = valid_tags(field=domain)
    cache[domain] = tags
    save_cache(cache=cache)
    return tags


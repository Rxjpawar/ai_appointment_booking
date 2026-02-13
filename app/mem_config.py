from dotenv import load_dotenv
from mem0 import Memory
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

config = {
    "version": "v1.1",

    #vector embedder
    # "embedder": {
    #     "provider": "openai",
    #     "config": {
    #         "api_key": OPENAI_API_KEY,
    #         "model": "text-embedding-3-small"
    #     }
    # },

    #llm
    "llm": {
        # "provider": "openai",
        "provider": "groq",
        "config": {
            "api_key": GROQ_API_KEY,
            "model": "meta-llama/llama-4-scout-17b-16e-instruct"
        },
        # "config": {
        #     "api_key": OPENAI_API_KEY,
        #     "model": "gpt-4o-mini"
        # }
    
    },

    #vector memory 
    # "vector_store": {
    #     "provider": "qdrant",
    #     "config": {
    #         "host": "localhost",
    #         "port": "6333"
    #     }
    # },

    #relationships  - missing part of my life 
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "reform-william-center-vibrate-press-5829"
        }
    },
}

mem_client = Memory.from_config(config)
import os
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs, and snippets."""
    results = tavily_client.search(query=query, max_results=5)
    out = []
    for r in results.get("results", []):
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content'][:300]}")
    return "\n---\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove noisy tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
            
        text = soup.get_text(separator=" ")
        # Return a restricted character count to save LLM tokens
        return text[:3000] 
    except Exception as e:
        return f"Could not scrape {url}: {str(e)}"
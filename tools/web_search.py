from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """
    Searches the web using DuckDuckGo.
    Use this to find documentation, latest news, or any information on the internet.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No results found."
            
        formatted_results = []
        for i, res in enumerate(results):
            formatted_results.append(f"{i+1}. Title: {res.get('title')}\nURL: {res.get('href')}\nSnippet: {res.get('body')}\n")
            
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

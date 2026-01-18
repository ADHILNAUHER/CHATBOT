from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain.tools import tool

search = DuckDuckGoSearchResults()

@tool
def search_the_web(query: str) -> str:
    """Use this to search the web for relevant information."""
    return search.invoke(query)
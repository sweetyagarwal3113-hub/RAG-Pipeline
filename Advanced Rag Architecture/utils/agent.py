from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.tools.retriever import create_retriever_tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def create_rag_agent(llm, retriever):
    # Create a Tool out of our massive advanced retriever pipeline
    retriever_tool = create_retriever_tool(
        retriever,
        "knowledge_base_search",
        "Search for information about the user's document. Always use this tool if you need factual information."
    )
    
    # Add a Web Search Tool and RESTRICT its output size to avoid hitting Groq Token limits!
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=2)
    web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    web_search.name = "web_search"
    web_search.description = "Search the internet for current events, news, or factual information that is NOT in the knowledge base."
    
    tools = [retriever_tool, web_search]

    # Create the agent prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. You have access to a knowledge base tool and a web search tool. Today's date is July 2026. You MUST use the web search tool to find answers for any current events or factual questions that you do not confidently know. NEVER refuse to answer without searching the web first!"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Construct the Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.tools.retriever import create_retriever_tool

def create_rag_agent(llm, retriever):
    # Create a Tool out of our massive advanced retriever pipeline
    retriever_tool = create_retriever_tool(
        retriever,
        "knowledge_base_search",
        "Search for information about the user's document. Always use this tool if you need factual information."
    )
    tools = [retriever_tool]

    # Create the agent prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. You have access to a knowledge base tool. Use it whenever you need to answer questions about the document."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # Construct the Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

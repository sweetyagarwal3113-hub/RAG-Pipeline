from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""

You are a helpful AI assistant. 

First, try to answer the question using the provided context. 

If the answer is not found in the context, you may use your general knowledge to answer the question, but briefly mention that the answer is not from the provided document.

Context:

{context}

Question:

{input}

""")
from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0,
    max_retries=2,
)
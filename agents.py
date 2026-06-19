from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def build_search_agent():
    # The new standard natively handles the loop and system mapping
    return create_agent(model=llm, tools=[web_search])

def build_reader_agent():
    return create_agent(model=llm, tools=[scrape_url])

# Writer Chain utilizing LCEL Pipe syntax
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional research writer. Draft clear, well-structured, and insightful reports based on the provided context."),
    ("human", "Topic: {topic}\n\nGathered Research:\n{research}\n\nStructure the report with an Introduction, Key Findings (minimum 3), a Conclusion, and a Sources list.")
])
writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain utilizing LCEL Pipe syntax
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp, constructive research critic. You evaluate reports honestly and specifically."),
    ("human", "Review the report below. Provide a score out of 10, outline strengths, identify areas for improvement, and give a one-line verdict.\n\nReport:\n{report}")
])
critic_chain = critic_prompt | llm | StrOutputParser()
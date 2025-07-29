from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key="###"  # Replace with your actual API key
    )

def nlp_to_sql(user_query:str)->str:

    schema = """
    You are an expert SQL generator. User will provide the table info if dont't return general query assuming table.
    Only return the SQL query — do not explain.
    """

    
    prompt = ChatPromptTemplate.from_template(
        "{schema}\n\nQuestion: {question}\nSQL:"
    )
  
    chain = prompt | llm
    
    response = chain.invoke({'schema':schema, 'question':user_query})
    print(response)
    return response.content

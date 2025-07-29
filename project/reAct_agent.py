from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from quizGenerator import generate_quiz
from nlpToSql import nlp_to_sql
import tempfile
import re
from langchain_community.document_loaders import PyPDFLoader,TextLoader, UnstructuredWordDocumentLoader
from langchain.tools import Tool
import os
from RAG_FAQ import find_answer
from langchain_community.document_loaders import PyPDFLoader
from pymongo import MongoClient
from datetime import datetime
from langchain_core.messages import HumanMessage,AIMessage


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)

db = client["QUERYLY"]
chat_history = db["CHAT_HISTORY"]

tools = [
Tool(
    name="quiz-generator",
    description="It takes sql topic from user and generate quiz for the user to help him prepare for his work",
    func = generate_quiz
),
Tool(
    name="nlp-to-sql",
    description="It takes natural language query of user and generates it to sql syntax query",
    func = nlp_to_sql
),
Tool(
    name="rag-faq",
    description="It takes two things a document and a query. And answer questions about that document. Preventing hallucinations",
    func = find_answer
)
]

llm = ChatOpenAI(model = "gpt-4")


agent = create_react_agent(
    model = llm,
    tools = tools,
    prompt = """
    You are an intelligent assistant for SQL based learning with access to specialized tools. 
    
    Basically a SQL Learning platform!

    1- quiz-generator (It generates quiz for user on any SQL related topic)
    Schema --> Input (topic: str) & output (Quiz)

    2- nlp-to-sql (It takes user natural language query understands it and convert to SQL query)
    Schema --> Input (user_query:str) & output (str)

    3- rag-faq (It takes user document and query and answers the questions related to that query)
    Schema --> Input (document, query:str) & output(str)
    example - if user message contains context of document (It is going to use this tool)

    Note: If user just asks question anything about SQL and you dont't
    think that there is need to call any tool, just answers within your capabilities
    And keep in mind that you are SQL Instructor. If user asks any other domain related
    question just say I can help with SQL only!

    Keep schema in mind!
    """   
)

def answer_query(file,query:str):
    

    #If query uploads document
    docs = []
    loader = None
    if file is not None and query is not None:
        suffix = os.path.splitext(file.name)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(file.read())
            temp_file_path = tmp_file.name

            if suffix == ".pdf":
                loader = PyPDFLoader(temp_file_path)
            elif suffix == ".docx":
                loader = UnstructuredWordDocumentLoader(temp_file_path)
            elif suffix == ".txt":
                loader = TextLoader(temp_file_path,encoding='utf-8')
            else:
                raise Exception("error")
        docs = loader.load()
        document_text = "\n".join([doc.page_content for doc in docs])
        query = query + f"Here is the related document context: {document_text}"



    messages = []
    my_msg = query
    messages.append(query)
    response = agent.invoke({
        "messages": messages
    })
    messages_list = response.get("messages", [])

    ai_msg = ""
    for msg in reversed(messages_list):
        if isinstance(msg, AIMessage) and msg.content:
            ai_msg = msg.content
            break

    # Save to MongoDB
    chat_history.insert_one({
    "timestamp": datetime.utcnow(),
    "chat": [
        {"type": "human", "content": my_msg},
        {"type": "ai", "content": ai_msg}
        ]
    })
    
    return ai_msg

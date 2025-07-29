from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def find_answer(docs, query):
    chunker = SemanticChunker(
        embeddings=OpenAIEmbeddings(),
        breakpoint_threshold_type="standard_deviation",
        breakpoint_threshold_amount=1
    )

    chunks = chunker.split_documents(docs)

    # ✅ Use Chroma vector store instead of FAISS
    persist_directory = "./chroma_db"  # You can also keep it in-memory
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_directory
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "lambda_mult": 1}
    )

    results = retriever.invoke(query)

    prompt = PromptTemplate(
        template="""
        You are an expert at providing correct answers to user queries. 
        I will provide you with both context and query, so answer accordingly.
        
        Query: {query}
        Context: {context}
        """,
        input_variables=["query", "context"]
    )

    model = ChatOpenAI(model="gpt-4")
    parser = StrOutputParser()
    chain = prompt | model | parser
    finalized = chain.invoke({'query': query, 'context': results})

    return finalized


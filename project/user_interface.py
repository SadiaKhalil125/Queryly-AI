import streamlit as st
from reAct_agent import answer_query, chat_history # Assumed to be your backend file


st.set_page_config(
    page_title="Queryly AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    st.markdown("""
        <style>
            /* --- General Styles --- */
            body {
                color: #EAEAEA;
            }
            .main {
                background-color: #0E1117;
                border-radius: 20px;
            }
            .st-emotion-cache-18ni7ap { /* Main container */
                background-color: #0E1117;
            }

            /* --- Sidebar Styling --- */
            [data-testid="stSidebar"] {
                background-color: #1A1C24;
                border-right: 1px solid #2C2F38;
            }
            [data-testid="stSidebar"] .st-emotion-cache-16txtl3 { /* Sidebar content */
                color: #EAEAEA;
            }
            .st-emotion-cache-dvne4q { /* Sidebar Header */
                 font-family: 'Arial', sans-serif;
                 font-weight: 600;
            }

            /* --- Chat Bubble Styling --- */
            .st-emotion-cache-1c7y2kd { /* User message container */
                background-color: #262730;
                border: 1px solid #3A3C46;
                border-radius: 12px;
                padding: 1rem;
            }
            .st-emotion-cache-4oy321 { /* Assistant message container */
                background-color: #1B2941; /* Slightly different background for assistant */
                border: 1px solid #2A3C5B;
                border-radius: 12px;
                padding: 1rem;
            }
            
            /* --- Tool Template Expanders --- */
            .st-expander {
                border: 1px solid #2C2F38 !important;
                border-radius: 10px !important;
                background-color: #1A1C24 !important;
            }
            .st-expander > summary {
                color: #6C99EE !important;
                font-weight: 600;
                font-size: 1.1rem;
            }
            .st-expander > summary:hover {
                color: #88AEF1 !important;
            }

            /* --- File Uploader --- */
            [data-testid="stFileUploader"] {
                border: 2px dashed #2C2F38;
                background-color: #1A1C24;
                border-radius: 10px;
                padding: 1rem;
            }
            [data-testid="stFileUploader"] label {
                font-weight: 600;
                color: #6C99EE;
            }
            
            /* --- Main Title & Caption --- */
            .st-emotion-cache-10trblm { /* Main Title */
                font-size: 2.5rem;
                font-weight: 700;
                color: #FFFFFF;
            }
            .st-emotion-cache-1xarl3l { /* Main Caption */
                color: #A0A0A0;
            }

        </style>
    """, unsafe_allow_html=True)

load_css()



with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #6C99EE;'>Queryly AI ⚡</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("📄 Document Analysis (RAG)")
    uploaded_file = st.file_uploader(
        "Upload a Document (.pdf, .docx, .txt)",
        type=["pdf", "docx", "txt"],
        help="Upload a document to ask specific questions about its content.",
        label_visibility="collapsed"
    )
    st.markdown("---")

    st.subheader("🚀 Tool Templates")
    st.caption("Use these examples to interact with the tools.")

    with st.expander("❓ Quiz Generator"):
        st.info("Generates a multiple-choice quiz on any SQL topic.")
        st.code("I want to attempt quiz on Data Definition Language in SQL")

    with st.expander("🧑‍💻 NLP-to-SQL Converter"):
        st.info("Converts your plain English into a valid SQL query.")
        st.code("""Show the names and salaries of employees in the HR department.
Table: Employees(ID, Name, Department, Salary, JoiningDate)""")

    with st.expander("🔍 Document Q&A"):
        st.info("Answers questions based on your uploaded document.")
        st.code("Based on the document, what is the main conclusion?")


# --- Main Chat Interface ---
st.title("💬 Your Intelligent SQL Assistant")
st.caption("I can generate quizzes, convert natural language to SQL, or answer questions about your documents.")

# Initialize or load chat history from session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        history_from_db = chat_history.find().sort("timestamp")
        for record in history_from_db:
            for message in record.get("chat", []):
                role = "user" if message["type"] == "human" else "assistant"
                st.session_state.messages.append({"role": role, "content": message["content"]})
    except Exception as e:
        st.error(f"Failed to load chat history: {e}")

# Display all messages from session state
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask me anything about SQL..."):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Get and display assistant response
    with st.spinner("🧠 Thinking..."):
        response = answer_query(uploaded_file, prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
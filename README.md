# Queryly AI - Intelligent SQL Learning Platform ⚡

## 🎯 Project Overview

Queryly AI is a comprehensive SQL learning platform that combines multiple AI-powered tools to provide an interactive and intelligent learning experience. The platform features a ReAct agent with 4 specialized tools, a modern Streamlit interface, and MongoDB integration for persistent chat history.

## 🏗️ Architecture & Components

### Core System Architecture
- **Backend**: Python-based with LangChain framework
- **Frontend**: Streamlit web application with custom CSS styling
- **Database**: MongoDB for chat history persistence
- **AI Models**: OpenAI GPT-4, Llama 3.1 70B (via Groq), and HuggingFace models
- **Agent Framework**: LangGraph ReAct agent with tool orchestration

## 🤖 ReAct Agent Implementation

The ReAct agent serves as the central intelligence hub with **4 specialized tools**:

### 1. **NLP-to-SQL Converter** (`nlpToSql.py`)
- **Model**: Llama 3.1 70B (8192 context) via Groq API
- **Function**: Converts natural language queries to SQL syntax
- **Input**: Natural language description of desired SQL operation
- **Output**: Valid SQL query string
- **Features**:
  - Handles table schema information when provided
  - Generates general queries when table info is not specified
  - Uses structured prompt templates for consistent output

### 2. **Quiz Generator** (`quizGenerator.py`)
- **Model**: OpenAI GPT-4o (2024-08-06) with temperature 1.3
- **Function**: Generates comprehensive SQL quizzes on any topic
- **Input**: SQL topic string
- **Output**: Structured Quiz object with 10 multiple-choice questions
- **Features**:
  - Generates exactly 10 unique questions per quiz
  - Each question has 4 options with 1 correct answer
  - Includes metadata with table schemas when relevant
  - Minimum passing score: 8/10
  - Structured output using Pydantic models

### 3. **RAG FAQ System** (`RAG_FAQ.py`)
- **Model**: OpenAI GPT-4 for answer generation
- **Embeddings**: OpenAI Embeddings for semantic search
- **Vector Store**: Chroma with MMR (Maximum Marginal Relevance) retrieval
- **Function**: Answers questions based on uploaded documents
- **Input**: Document content and user query
- **Output**: Context-aware answers preventing hallucinations
- **Features**:
  - Semantic chunking using OpenAI embeddings
  - Chroma vector database with persistent storage (`./chroma_db`)
  - MMR retrieval with k=3 documents
  - Context-aware answer generation
  - Supports PDF, DOCX, and TXT files
  - Persistent document storage for improved performance
  - Automatic document indexing and retrieval

### 4. **General SQL Assistant**
- **Model**: OpenAI GPT-4
- **Function**: Provides general SQL knowledge and explanations
- **Scope**: SQL-only domain expertise
- **Features**:
  - Direct knowledge-based responses
  - No tool invocation for general SQL questions
  - Domain-specific focus (SQL only)

## 📊 Data Models

### Quiz System Models
```python
# Quiz.py - Main quiz container
class Quiz(BaseModel):
    questions_count: int = 10
    questions: List[Question]
    min_passing_marks: int = 8
    meta_data: Optional[str] = None

# Question.py - Individual question structure
class Question(BaseModel):
    topic: str
    description: str
    options: List[Option]
    correct_option_id: int

# Option.py - Multiple choice options
class Option(BaseModel):
    description: str
```

### User Management Models
```python
# User.py - User account information
class User(BaseModel):
    name: str = Field(description="Name of user")
    email: str = Field(description="Email of user")
    password: str = Field(description="password for user's account")

# QuizGeneratorReq.py - Quiz generation request
class QuizRequest(BaseModel):
    topic: str
```

## 🎨 User Interface (Streamlit)

### Design Features
- **Modern Dark Theme**: Professional dark UI with custom CSS
- **Responsive Layout**: Wide layout with expandable sidebar
- **Chat Interface**: Real-time chat with user/assistant avatars
- **File Upload**: Support for PDF, DOCX, and TXT documents
- **Tool Templates**: Pre-built examples for each tool
- **Persistent Chat History**: MongoDB integration for conversation continuity

### UI Components
1. **Sidebar**:
   - Document upload interface
   - Tool template examples
   - Quick access to different functionalities

2. **Main Chat Area**:
   - Real-time message display
   - Loading indicators
   - Avatar-based message distinction

3. **Custom Styling**:
   - Dark theme with blue accents (#6C99EE)
   - Rounded corners and modern borders
   - Professional typography

## 🔧 Technical Implementation Details

### Agent Orchestration (`reAct_agent.py`)
```python
# Tool definitions with specific schemas
tools = [
    Tool(name="quiz-generator", description="...", func=generate_quiz),
    Tool(name="nlp-to-sql", description="...", func=nlp_to_sql),
    Tool(name="rag-faq", description="...", func=find_answer)
]

# LangGraph ReAct agent with custom prompt
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="..." # SQL-focused instruction prompt
)
```

### Document Processing Pipeline
1. **File Upload**: Streamlit file uploader with type validation
2. **Document Loading**: PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
3. **Temporary Storage**: Secure temporary file handling
4. **Content Extraction**: Text extraction and concatenation
5. **Semantic Chunking**: OpenAI embeddings-based document segmentation
6. **Vector Storage**: Chroma database with persistent storage (`./chroma_db`)
7. **Context Integration**: Document content appended to user query

### Chat History Management
- **MongoDB Integration**: Persistent storage of all conversations
- **Timestamp Tracking**: UTC timestamps for each interaction
- **Session State**: Streamlit session state for real-time chat
- **History Loading**: Automatic loading of previous conversations

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB instance
- OpenAI API key
- Groq API key

### Environment Variables
Create a `.env` file with:
```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
MONGO_URI=mongodb://localhost:27017/
```

### Installation Steps
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MongoDB connection
4. Configure environment variables
5. Run the application: `streamlit run user_interface.py`

### Database Setup
- **MongoDB**: Required for chat history persistence
- **Chroma**: Automatically creates `./chroma_db` directory for document storage
- No additional setup required for Chroma - handles initialization automatically

## 📦 Dependencies

The project uses the following key libraries:
- **LangChain**: AI framework and tool orchestration
- **LangGraph**: ReAct agent implementation
- **Streamlit**: Web interface framework
- **OpenAI**: GPT-4 and embeddings
- **Groq**: Llama 3.1 70B access
- **MongoDB**: Database for chat history
- **Chroma**: Vector database for document storage and retrieval
- **Pydantic**: Data validation and serialization

## 🎯 Key Features

### 1. **Intelligent Tool Selection**
- Automatic tool selection based on user intent
- Context-aware responses
- Fallback to general SQL knowledge

### 2. **Multi-Modal Document Support**
- PDF document processing
- Word document (.docx) support
- Plain text file handling
- Semantic chunking for optimal retrieval
- Persistent Chroma vector storage for document indexing

### 3. **Structured Quiz Generation**
- Topic-specific quiz creation
- Multiple choice format with explanations
- Configurable difficulty and question count
- Metadata inclusion for context

### 4. **Natural Language to SQL**
- Advanced LLM-powered conversion
- Schema-aware query generation
- Support for complex SQL operations

### 5. **Persistent Learning Experience**
- Chat history across sessions
- User progress tracking
- Contextual conversation continuity

## 🔍 Usage Examples

### Quiz Generation
```
User: "I want to attempt quiz on Data Definition Language in SQL"
Agent: Generates 10 multiple-choice questions on DDL with explanations
```

### NLP-to-SQL Conversion
```
User: "Show the names and salaries of employees in the HR department"
Agent: SELECT name, salary FROM employees WHERE department = 'HR';
```

### Document Q&A
```
User: "Based on the uploaded document, what is the main conclusion?"
Agent: Analyzes document content and provides context-aware answer
```

## 🛠️ Development & Customization

### Adding New Tools
1. Create tool function in separate module
2. Add tool definition to `tools` list in `reAct_agent.py`
3. Update agent prompt with tool description
4. Test integration

### Model Configuration
- Change LLM models in respective modules
- Adjust temperature and other parameters
- Configure API endpoints and keys

### UI Customization
- Modify CSS in `user_interface.py`
- Add new Streamlit components
- Customize color scheme and layout

## 📈 Performance & Scalability

### Current Performance
- **Response Time**: 2-5 seconds for most operations
- **Document Processing**: Supports files up to 10MB
- **Concurrent Users**: Streamlit handles multiple sessions

### Scalability Considerations
- MongoDB connection pooling
- Chroma vector store optimization and persistence
- API rate limiting
- Caching strategies
- Document indexing and retrieval optimization

## 🔒 Security & Privacy

### Data Handling
- Temporary file cleanup
- Secure API key management
- MongoDB connection security
- User data privacy protection

### Best Practices
- Environment variable usage
- Input validation
- Error handling
- Secure file processing

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create GitHub issue
- Check documentation
- Review error logs

---

**Queryly AI** - Empowering SQL learning through intelligent AI assistance ⚡ 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from models.Question import Question
from models.Option import Option
from models.Quiz import Quiz
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()



llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=1.3)
model = llm.with_structured_output(Quiz)

def generate_quiz(topic: str)->Quiz:
    prompt = PromptTemplate(
        template="""
You are an intelligent SQL quiz generator.

Generate a multiple-choice quiz on the topic: "{topic}". The quiz should meet the following conditions:

- Generate exactly 10 unique questions.
- Each question should have:
    - A clear `description` (question text).
    - A list of 4 options.
    - Only one correct option (`correct: true`).
    - A `correct_option_id` (integer between 1-4) (among those 4 of the question's options).
    - A `meta_data` field:
        - If the question is based on a SQL table, include the table schema or sample data as a string in `meta_data`. 
          Example:
          ```
          Table: Employees(id INT, name VARCHAR, salary INT)
          ```
        - Otherwise, keep `meta_data` as an empty string.

- All questions must be relevant to "{topic}".
- Set:
    - `questions_count` = 10
    - `min_passing_marks` = 8

Output only structured data. Do not include explanations.
""",
input_variables=['topic']
    )
    chain = prompt | model
    result = chain.invoke(prompt)
    return result

# print(generate_quiz('SELECT CLAUSE'))



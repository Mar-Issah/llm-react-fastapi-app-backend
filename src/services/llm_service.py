from langchain_anthropic import ChatAnthropic
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from typing_extensions import Annotated, TypedDict
from typing import List

load_dotenv()

os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"


class ChallengeLLMOutput(TypedDict):
    title: Annotated[str, "The question title"]
    options: Annotated[List[str], "List of possible answer choices"]
    correct_answer_id: Annotated[
        int, "Index of the correct answer in the options list (0-3)"
    ]
    explanation: Annotated[
        str, "Detailed explanation of why the correct answer is right"
    ]


llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.9,
)


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator.
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure with the following fields:
    - title: A complete question, written as a full sentence. This will be shown directly to the user.
    - options: A list of 4 possible answer choices
    - correct_answer_id: Index of the correct answer in the options list (0-3)
    - explanation: A detailed explanation of why the correct answer is right. Ensure the explanation is clearly written and well-formatted with line breaks where appropriate for readability. Use bullet points, step-by-step reasoning, or short paragraphs to explain the logic

    Make sure the options are plausible but with only one clearly correct answer.

    Apply proper operator precedence rules (PEMDAS/BODMAS) when evaluating mathematical expressions in Python. All questions and answers must be verified by running the Python code before returning a response.
    """
    try:
        # Adding output parser
        parser = PydanticOutputParser(pydantic_object=ChallengeLLMOutput)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", f"Generate a {difficulty} difficulty coding challenge."),
            ]
        )

        chain = prompt | llm.with_structured_output(ChallengeLLMOutput)
        response = chain.invoke({"difficulty": difficulty})
        return response
    except Exception as e:
        print(e)
        return {
            "title": "Basic Python List Operation",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)",
                "my_list.insert(5)",
            ],
            "correct_answer_id": 0,
            "explanation": "In Python, append() is the correct method to add an element to the end of a list.",
        }

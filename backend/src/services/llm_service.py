from langchain_anthropic import ChatAnthropic
import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
# from ..schemas.challenge import ChallengeLLMOutput

load_dotenv()

# os.environ.get("LANGCHAIN_API_KEY")
# os.environ["LANGSMITH_TRACING"] = ("true")

class ChallengeLLMOutput(BaseModel):
    title: str = Field(..., description="The question title")
    options: List[str] = Field(..., description="List of possible answer choices")
    correct_answer_id: int = Field(
        ..., description="Index of the correct answer in the options list (0-3)"
    )
    explanation: str = Field(..., description="Detailed explanation of why the correct answer is right")


llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.6,

)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator.
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:{format_instructions}

    Make sure the options are plausible but with only one clearly correct answer.
    """
    try:
        # Adding output parser
        parser = PydanticOutputParser(pydantic_object=ChallengeLLMOutput)

        prompt = ChatPromptTemplate.from_messages([
                ("system",  system_prompt),
                ("human",f"Generate a {difficulty} difficulty coding challenge."),
            ]).partial(format_instructions=parser.get_format_instructions())

        chain = prompt | llm | parser
        response = chain.invoke(
            {
               "difficulty": difficulty
            }
        )
        return response

            # response_format={"type": "json_object"},
            # temperature=0.7,
        # )

        # content = response.choices[0].message.content
        # challenge_data = json.loads(content)

        # required_fields = ["title", "options", "correct_answer_id", "explanation"]
        # for field in required_fields:
        #     if field not in challenge_data:
        #         raise ValueError(f"Missing required field: {field}")

        # return challenge_data

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

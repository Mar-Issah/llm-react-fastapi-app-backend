from pydantic import BaseModel, Field
from typing import List


class ChallengeRequest(BaseModel):
    """
    Request schema for generating a challenge
    Args:
        difficulty (str): The difficulty level of the challenge (e.g., "easy", "medium", "hard")
    """

    difficulty: str

    class Config:
        json_schema_extra = {"example": {"difficulty": "easy"}}



class ChallengeLLMOutput(BaseModel):
    title: str = Field(..., description="The question title")
    options: List[str] = Field(..., description="List of possible answer choices")
    correct_answer_id: int = Field(
        ..., description="Index of the correct answer in the options list (0-3)"
    )
    explanation: str = Field(..., description="Detailed explanation of why the correct answer is right")

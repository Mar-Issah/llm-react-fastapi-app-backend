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



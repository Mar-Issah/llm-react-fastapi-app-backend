from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db import Base


# Below are the models for the database tables. They need to inherit from Base so that SQLAlchemy can manage them.
class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    created_by = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)


class ChallengeQuota(Base):
    __tablename__ = "challenge_quotas"

    # user_id: this is a unique identifier for each user, usually coming from your auth provider (like Clerk).
    # It ensures each user can have only one quota record.
    # The unique=True constraint enforces that — 1 quota per user.
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, default=datetime.now)

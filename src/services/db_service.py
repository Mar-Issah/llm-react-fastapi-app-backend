from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.database import models


#  The db function always take the db as first arg
def get_challenge_quota(db: Session, user_id: str):
    """
    Get the challenge quota for a user
    """
    return (
        db.query(models.ChallengeQuota)
        .filter(models.ChallengeQuota.user_id == user_id)
        .first()
    )


def create_challenge_quota(db: Session, user_id: str):
    """
    Create a new challenge quota for a user
    """
    db_quota = models.ChallengeQuota(user_id=user_id)
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota


def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    """
    Reset the quota if it has been more than 24 hours since the last reset.
    """
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.quota_remaining = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota


def create_challenge(
    db: Session,
    difficulty: str,
    created_by: str,
    title: str,
    options: str,
    correct_answer_id: int,
    explanation: str,
):
    """
    Create a new challenge
    """
    db_challenge = models.Challenge(
        difficulty=difficulty,
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation,
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_user_challenges(db: Session, user_id: str):
    """
    Get all challenges created by a user
    """
    return (
        db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()
    )

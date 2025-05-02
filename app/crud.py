import uuid

from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas


def get_user_by_username(db: Session, username: str) -> models.User | None:
    """Получить пользователя по username"""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str):
    db_user = models.User(
        username=username,
        token=str(uuid.uuid4())
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def validate_user(db: Session, user_id: int, token: UUID):
    return db.query(models.User).filter(
        models.User.id == user_id,
        models.User.token == str(token)
    ).first()


def get_audio(db: Session, audio_id: str, user_id: int):
    return db.query(models.Audio).filter(
        models.Audio.id == audio_id,
        models.Audio.user_id == user_id
    ).first()


def create_audio(
        db: Session,
        audio_id: str,
        user_id: int,
        file_path: str
) -> models.Audio:
    db_audio = models.Audio(
        id=audio_id,
        user_id=user_id,
        file_path=file_path
    )
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import UUID4
import os
import uuid
from pathlib import Path

from fastapi import Request
from . import models, schemas, crud, utils
from .database import SessionLocal, engine, get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    Path("uploads").mkdir(exist_ok=True)
    models.Base.metadata.create_all(bind=engine)


@app.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    if db_user := crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    return crud.create_user(db=db, username=user.username)


@app.post("/audios/", response_model=schemas.AudioResponse)
async def create_audio(
        request: Request,
        user_id: int = Form(...),
        token: UUID4 = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    user = crud.validate_user(db, user_id, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if file.content_type not in ['audio/wav', 'audio/wave']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only WAV files are allowed"
        )

    try:
        audio_id = await utils.process_audio(file, user_id)

        mp3_filename = f"{user_id}_{audio_id}.mp3"
        db_audio = crud.create_audio(
            db=db,
            audio_id=audio_id,
            user_id=user_id,
            file_path=f"uploads/{mp3_filename}"
        )

        base_url = str(request.base_url).rstrip('/')
        download_url = f"{base_url}/record?id={audio_id}&user={user_id}"

        return {"download_url": download_url}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/record")
async def download_audio(
        id: UUID4,
        user: int,
        db: Session = Depends(get_db)
):
    audio = crud.get_audio(db, audio_id=str(id), user_id=user)
    if not audio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio not found"
        )

    file_path = Path(audio.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=f"audio_{id}.mp3"
    )

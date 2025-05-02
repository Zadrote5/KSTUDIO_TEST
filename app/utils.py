import tempfile
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from pydub import AudioSegment


async def process_audio(file: UploadFile, user_id: int) -> str:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)

    audio_id = uuid.uuid4()
    mp3_filename = f"{user_id}_{audio_id}.mp3"
    mp3_path = uploads_dir / mp3_filename

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            audio = AudioSegment.from_file(tmp.name)
            audio.export(
                mp3_path,
                format="mp3",
                bitrate="192k"
            )

        return str(audio_id)
    finally:
        if Path(tmp.name).exists():
            Path(tmp.name).unlink()


async def is_valid_wav(file_path: Path) -> bool:
    """
    Проверяет базовую структуру WAV-файла
    """
    try:
        with file_path.open('rb') as f:
            header = f.read(4)
            if header != b'RIFF':
                return False

            f.seek(8)
            format = f.read(4)
            return format == b'WAVE'

    except Exception as e:
        return False

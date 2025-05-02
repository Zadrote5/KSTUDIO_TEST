from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)

class UserResponse(BaseModel):
    id: int
    username: str
    token: str
    model_config = ConfigDict(from_attributes=True)

class AudioResponse(BaseModel):
    download_url: str
    model_config = ConfigDict(from_attributes=True)
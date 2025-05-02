from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    token: Mapped[str] = mapped_column(String(36), unique=True)

    audios: Mapped[list["Audio"]] = relationship(back_populates="user")
    __table_args__ = (
        UniqueConstraint('username', name='uq_username'),
    )


class Audio(Base):
    __tablename__ = "audios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    file_path: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="audios")

from flask_login import UserMixin
from app import db  # Absolute import from app package
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
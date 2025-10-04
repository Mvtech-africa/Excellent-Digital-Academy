from flask_login import UserMixin
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    tos: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # --1 to 1 relationship
    profile = relationship[Optional["Profile"]] = relationship(back_populates="user")


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"

class Profile(db.Model):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[Optional[str]]
    avatar_url : Mapped[Optional[str]]
    user_id : Mapped[int] = mapped_column(db.ForeignKey('user.id'), unique=True)
    user: Mapped['User'] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile(id={self.id!r}"
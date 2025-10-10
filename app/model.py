from flask_login import UserMixin
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Float
from typing import Optional,  List
from datetime import date


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    tos: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ✅ 1-to-1 relationship
    profile: Mapped[Optional["Profile"]] = relationship(
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
)

    courses: Mapped[List["Course"]] = relationship(
    back_populates="instructor",
    cascade="all, delete-orphan"
)


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Profile(db.Model):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    country_of_origin: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    state_of_origin: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    lg_of_origin: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    country_of_residence: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    state_of_residence: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    lg_of_residence: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True, nullable=False)

    # Relationship back to User
    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile(id={self.id!r}, user_id={self.user_id!r})"


class Course(db.Model):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String(5000), nullable=True)
    instructor_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # renamed ✅
    duration: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    date_enrolled: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_ended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    instructor_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    instructor: Mapped["User"] = relationship(back_populates="courses")  # keep this name ✅

    def __repr__(self) -> str:
        return f"<Course id={self.id} title='{self.title}'>"

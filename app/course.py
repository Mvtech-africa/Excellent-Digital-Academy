from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required , current_user
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from .model import User, Profile, Role
import os
from app import db
course = Blueprint('course', __name__)
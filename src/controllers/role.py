from flask import Blueprint, request
from sqlalchemy import inspect
from src.app import Role, Post, db
from http import HTTPMethod, HTTPStatus
from flask_jwt_extended import create_access_token


app = Blueprint('role', __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED
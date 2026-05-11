from flask import Blueprint, request, jsonify
from models.models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.json

    hashed_password = generate_password_hash(data['password'])

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User Registered Successfully"})


@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.json

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login Successful"})

    return jsonify({"message": "Invalid Credentials"})
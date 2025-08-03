from flask import Blueprint, request, jsonify
# import json 
from models.user_model import (
    fetch_all_users, fetch_user_by_id,create_user,
    update_user, delete_user, search_user_by_name,
    validate_login
)

user_bp = Blueprint('user',__name__)

# GET / - Health check
@user_bp.route('/')
def home():
    return "User Management System"

# GET /users - Get all users
@user_bp.route('/users',methods=['GET'])
def get_all_users():
    users = fetch_all_users()
    return jsonify(users)

# GET /user/<id> - Get specific user
@user_bp.route('/users/<user_id>',methods=['GET'])
def get_user(user_id):
    user = fetch_user_by_id(user_id)
    return jsonify(user) if user else ("User not found",404)

# POST /users - Create new user
@user_bp.route("/users",methods=['POST'])
def post_user():
    data = request.get_json()
    create_user(data['name'],data['email'],data['password'])
    return 'User created',201

# PUT /user/<id> - Update user
@user_bp.route('/user/<user_id>',methods=['PUT'])
def put_user(user_id):
    data = request.get_json()
    if data.get('name') and data.get('email'):
        update_user(user_id,data['name'],data['email'])
        return 'User updated'
    return "Invalid data",400

# DELETE /user/<id> - Delete user
@user_bp.route('/user/<user_id>',methods=['DELETE'])
def delete_user_route(user_id):
    delete_user(user_id)
    return f"User {user_id} delete"

# GET /search?name=<name> - Search users by name
@user_bp.route('/search',methods=['GET'])
def search_users():
    name= request.args.get('name')
    if not name:
        return 'Please provide a name to search', 400
    users = search_user_by_name(name)
    return jsonify(users)

# POST /login - User login
@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = validate_login(data['email'],data['password'])
    return jsonify({"status":"success","user_id":user[0]}) if user else jsonify({"status":"failed"})
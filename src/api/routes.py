"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def handle_login():

    body = request.json
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if body is None: 
        return jsonify("Your request is null"), 400
    if email is None: 
        return jsonify("Your request is missing an email"), 400
    if password is None: 
        return jsonify("Your request is missing a password"), 400

    user = User.query.filter_by(email = email).first()
    if user is None:
        return jsonify("User not found"), 404

    if password != user.password:
        return jsonify("Username and password do not match"), 404

    response_body = {
        'message': 'its working',
        'user': user.serialize()
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def handle_signup():

    body = request.json
    email = request.json.get("email")
    password = request.json.get("password")


    if body is None: 
        return jsonify("Your request is null"), 400
    if email is None: 
        return jsonify("Your request is missing an email"), 400
    if password is None: 
        return jsonify("Your request is missing a password"), 400

    userCheck = User.query.filter_by(email = email).first()
    if userCheck is not None:
        return jsonify("email already in use"), 409
    
    user = User(email = email, password = password, is_active = True)
    db.session.add(user)
    db.session.commit()



    response_body = {
        'message': 'its working',
        'user': user.serialize()
    }

    return jsonify(response_body), 200
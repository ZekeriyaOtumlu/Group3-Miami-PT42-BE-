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


#Login with POST Method
@api.route('/login', methods=['POST'])
@cross_origin()

def signIn():
    if request.method == 'POST':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return 'Please Enter your email', 401
        if not password:
            return 'Please Enter your password', 401

    user = User.query.filter_by(email = email, password = password).first()
    if user is None:
            return 'Error: Could not find the User' , 402
    token = create_access_token(identity = user.id)
    print(token)
    return jsonify({
        "message" : "Successfully logged in.",
        "token" : token}), 200


# SignUp with POST Method
@api.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    if request.method == 'POST':
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if not email:
            return 'Please Enter your email', 401
        if not password:
            return 'Please Enter your password', 401
        
        email_query = User.query.filter_by(email=email).first()
        if email_query:
            return 'This email already exists' , 402

        user = User()
        user.email = email
        user.password = password
        user.is_active = True
        print(user)
        db.session.add(user)
        db.session.commit()

        response = {
            'msg': 'User added successfully',
            'email': email
        }
        return jsonify(response), 200
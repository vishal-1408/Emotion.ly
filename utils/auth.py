from functools import wraps
from flask import request,jsonify
import jwt,os
from models.user import UserModel
from dotenv import load_dotenv

load_dotenv()

def checkJWT(f):
    @wraps(f)
    def _checkJWT():
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)
            token = token.replace('Bearer ','')
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}),401

        try:
            print(os.environ.get("SECRET") )
            data =jwt.decode(token, os.environ.get("SECRET") , algorithms=["HS256"])
            print(data)
            current_user = UserModel.fetchById(data["userId"])
            if not current_user:
                return jsonify({'message': 'User Id is invalid!'}),401
        except:
            return jsonify({'message': 'token is invalid'}),401

        return f(current_user)
    return _checkJWT
from flask import Blueprint, json,jsonify,request
from models.user import UserModel
import os,sys,jwt
from utils.auth import checkJWT
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename


# try:
#     decode_token = jwt.decode(encoded_token, 'MySECRET goes here', algorithms=['HS256'])
#     print("Token is still valid and active")
# except jwt.ExpiredSignatureError:
#     print("Token expired. Get new one")
# except jwt.InvalidTokenError:
#     print("Invalid Token")

#refresh the token if it got expired!!

user = Blueprint('user', __name__)

@user.route('/auth/login',methods=["POST"])
def login():
    print("login")
    body = request.get_json()
    if not body["email"] or not body["password"]:
        return jsonify({"message":"All required details are not provided"}),400
    user = UserModel.fetchByEmail(body["email"])
    if user:
        print(type(user))
        if UserModel.checkPassword(user.password,body["password"]):
            token = jwt.encode({"userId":user.id,'exp': datetime.utcnow() + timedelta(seconds=24*60*60)}, os.environ.get('SECRET') ,  os.environ.get('JWT_ALGO'))
            return jsonify({"token":token}),200
        else:
            return jsonify({"message":"Passwords don't match!"}),400
    else:
        return jsonify({"message":"given email is not associated with any user!"}),400



@user.route('/auth/signup',methods=["POST"])
def signup():
        body = request.get_json()
        if not body["email"] or not body["password"] or not body["name"]:
            return jsonify({"message":"All required details are not provided"}),400
        user = UserModel(**body)
        user.saveToDB()
        token = jwt.encode({"userId":user.id,'exp': datetime.utcnow() + timedelta(seconds=24*60*60)}, os.environ.get('SECRET') ,  os.environ.get('JWT_ALGO'))
        return jsonify({"token":token}),201

@user.route('/user',methods=["GET"])
@checkJWT
def userDetails(user):
        return {"user":{"id":user.id,"email":user.email,"name":user.name,"avatar":user.avatar}}

@user.route('/user',methods=["POST"])
@checkJWT
def updateAvatar(user):
        from utils.s3 import uploadFile
        if 'image' not in request.files:
            return {"message":"no file sent"},400
        image=request.files['image']
        if image and allowed_file(image.filename,{'jpg','png','jpeg'}):
            imagename = secure_filename(image.filename)
            key='general/'+imagename
            uploadFile(os.environ.get('BUCKET'),key,image)
            avatar = os.environ.get('AVATAR_BASE_URL')+key
            user.avatar = avatar
            user.saveToDB()
            return {"avatarUrl":avatar}
        return {"message":"file format is not supported"},400


    


def allowed_file(filename,allowedExt):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExt
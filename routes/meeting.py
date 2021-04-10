from flask import Blueprint, json,jsonify,request
from models.user import UserModel
from models.meeting import MeetingModel
from models.participants import ParticipantModel
from utils.agora import startRecordingAgora
from utils.s3 import getResultFrom,finalAnalysis
import os,sys,jwt,time
import requests
from datetime import datetime,timedelta
from utils.auth import checkJWT
from utils.RtcTokenBuilder import RtcTokenBuilder
import string,random
from dotenv import load_dotenv
load_dotenv()

meeting = Blueprint('meeting', __name__)

@meeting.route('/meeting/create',methods=["GET"])
@checkJWT
def createMeeting(currentUser):
    print("created!!!")
    channel = ''
    for i in range(3):
	    a=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = 3))
	    channel+=a
	    if i!=2:
	        channel+='-'
    uid = currentUser.id
    appId= os.environ.get("APPID")
    expiredTime = int(time.time()) + 24*60*60
    token = RtcTokenBuilder.buildTokenWithUid(appId,os.environ.get("APP_CERTIFICATE"),channel,uid,1,expiredTime)
    # print(uid,appId,expiredTime,channel,token)
    meeting = MeetingModel(channel,uid)
    meeting.saveToDB()
    participant = ParticipantModel(token,meeting.id,uid)
    participant.saveToDB()
    print({"meetingDetails":{"channel":channel,"token":token,"mid":meeting.id}})
    return jsonify({"meetingDetails":{"channel":channel,"token":token,"mid":meeting.id,"uid":uid}}),201

@meeting.route('/meeting/join',methods=["POST"])
@checkJWT
def joinMeeting(currentUser):
    body = request.get_json()
    meeting = MeetingModel.fetchByChannel(body["channel"])
    if not meeting:
        return jsonify({"message":"Channel name doesn't exist"}),400
    uid = currentUser.id
    appId= os.environ.get("APPID")
    expiredTime = int(time.time()) + 24*60*60
    token = RtcTokenBuilder.buildTokenWithUid(appId,os.environ.get("APP_CERTIFICATE"),meeting.channel,uid,1,expiredTime)
    # Code for adding participants in the meeting!
    participant = ParticipantModel(token,meeting.id,uid)
    participant.saveToDB()
    return jsonify({"meetingDetails":{"channel":meeting.channel,"token":token,"mid":meeting.id,"uid":uid}}),200

@meeting.route('/meeting/recording',methods=["POST"])
@checkJWT
def startRecording(user):
  try:
    print("this is the error fucking hell")
    body = request.get_json()
    print(body["channel"])
    meeting = MeetingModel.fetchByChannel(body["channel"])
    if not meeting:
        return {"message":"invalid channel name"}
    result = startRecordingAgora(body["channel"],meeting.id,body["token"])
    return result,200
  except Exception as e:
      print(str(e))

@meeting.route('/meeting/analysis',methods=["POST"])
@checkJWT
def startAnalysis(user):
        body = request.get_json()
        getResultFrom.apply_async(args=[body["mid"],body["rid"],body["sid"]])
        return {"message":"Will be processing it in the backend!"},202


@meeting.route('/meeting/result',methods=["POST"])
@checkJWT
def passResult(user):
    body = request.get_json()
    a = finalAnalysis(body["mid"])
    if not a==None:
        return jsonify(a),200
    return jsonify({"message": "Invalid meeting Id"}),400


# @meeting.route('/meeting/uid',methods=["POST"])
# @checkJWT
# def updateUID(user):
#     body = request.get_json()
#     muid =body["muid"]
#     mid = body["mid"]
#     participant = ParticipantModel.fetchByMidAndUid(mid,user.id)
#     if not participant:
#         return {"message":"invalid info"},400
#     participant.muid = muid
#     participant.saveToDB()
#     return {"message":"saved"},200


import boto3
from models.participants import ParticipantModel
from models.user import UserModel
from ml.model import emotion
from agora import queryStatus
from dotenv import load_dotenv
load_dotenv()
import os
import time
import random
from app import client
import schedule

s3 = boto3.resource(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)
s3_client = boto3.client('s3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

def uploadFile(bucket,key,file):
    s3.Bucket(bucket).put_object(Key=key, Body=file)

def getList(mid):
    files =[]
    for bucket in s3.buckets.all():
        for obj in bucket.objects.filter(Prefix=str(mid)+"/"):
            uid = obj.key.split('__uid_s_')[1].split('__uid_e_video_')[0]
            files.append({"key":obj.key,"uid":uid})
    return files



def checkTie(e,emax):
    ranking = {"neutral":1,"happy":2,"surprise":3,"sad":4,"angry":5,"fear":6,"disgust":7}
    if ranking[e]>ranking[emax]:
        return e
    else:
        return emax

def maxEmotion(d):
    maxValue=-1
    max=""
    for x in d:
        if d[x]>maxValue:
            max=x
            maxValue=d[x]
        if d[x]==maxValue:
            max=checkTie(x,max)
    return max



def scheduledTask(mid,rid,sid):
    # return 1
    participants = {}
    files=getList(mid)
    # if len(files)==0:
    #     code = queryStatus(rid,sid)
    #     # if(codes!!!):
    #     # jobs = schedule.get_jobs(str(mid))
    #     # if len(jobs)>0:
    #     #schedule.cancel_job(job)
    #     return None

    print("what happened")
    for f in files:
        name=os.sep.join(['image','image'+str(time.time()).split(".")[0]+'.jpg'])
        key = f["key"]
        s3.Bucket('emotionly').download_file(key,name)
        print("done!!!!")
        #s3_client.download_file(os.environ.get('BUCKET'), str(key), name)
        print("DONE!!")
        print("buckets done")
        result = emotion(name)
        print("emotion:",result)
        os.remove(name)
        if f["uid"] not in participants:
            participants[f["uid"]]={"happy":0,"disgust":0,"surprise":0,"fear":0,"angry":0,"neutral":0,"sad":0}
            if not result==None:
                participants[f["uid"]][result]=1
        else:
            if not result==None:
                participants[f["uid"]][result]+=1
        s3.Object(os.environ.get('BUCKET'), f["key"]).delete()
    print("for the participants!!!!",participants)
    for p in participants:
        participant = ParticipantModel.fetchByMidAndUid(mid,p)
        if not participant:
            return -1
        participant.happy +=participants[p]["happy"]
        participant.disgust +=participants[p]["disgust"]
        participant.surprise +=participants[p]["surprise"]
        participant.fear +=participants[p]["fear"]
        participant.angry+=participants[p]["angry"]
        participant.neutral+=participants[p]["neutral"]
        participant.sad+=participants[p]["sad"]
        print(maxEmotion({"happy":participant.happy,"disgust":participant.disgust,"surprise":participant.surprise,"fear":participant.fear,"angry":participant.angry,"neutral":participant.neutral,"sad":participant.sad}))
        participant.max = maxEmotion({"happy":participant.happy,"disgust":participant.disgust,"surprise":participant.surprise,"fear":participant.fear,"angry":participant.angry,"neutral":participant.neutral,"sad":participant.sad})
        participant.saveToDB()
        print(participant.max)
    return {"message":"success"}

def finalAnalysis(mid):
    participants = ParticipantModel.fetchByMid(mid)
    if not len(participants)>0:
        return None
    data = {"happy":0,"disgust":0,"surprise":0,"fear":0,"angry":0,"neutral":0,"sad":0}
    total=0
    participantAnalysis=[]
    for x in participants:
      user = UserModel.fetchById(x.uid)
      if x.max:
        data[x.max]+=1
        total+=1
        participantAnalysis.append({"email":user.email,"max":x.max,"name":user.name,"avatar":user.avatar})
        print(participantAnalysis,data,total)
      participantAnalysis.append({"email":user.email,"max":"0","name":user.name,"avatar":user.avatar})

    percentages = {}
    for x in data:
        percentages[x]=(data[x]/total)*100
    return {"meetingAnalysis":percentages,"participantAnalysis":participantAnalysis}


# @client.task
# def getResultFrom(mid,rid,sid):
#     a = scheduledTask(mid,rid,sid)
#     if a==None:
#         return
#     schedule.every(10).minutes.do(scheduledTask,mid=mid,rid=rid,sid=sid).tag('tasks'+str(mid),str(mid))
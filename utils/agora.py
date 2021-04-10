import requests
from dotenv import load_dotenv
load_dotenv()
import os
from flask import jsonify
import json
import random
def storageConfig(mid):
    return {
          "accessKey": os.environ.get("AWS_ACCESS_KEY"),
          "region": 14,
          "bucket":  os.environ.get("BUCKET"),
          "secretKey":  os.environ.get("AWS_SECRET_KEY"),
          "vendor": 1,
          "fileNamePrefix": [str(mid)]
      }

def startRecordingAgora(channel,mid,token):
    try:
        
        print("entered ")
        #generate the uid
        recordId = random.randint(99,99999999)

        #acquire the resourceId
        url = "https://api.agora.io/v1/apps/{}/cloud_recording/acquire".format(os.environ.get("APPID"))

        payload = json.dumps({
        "cname": channel,
        "uid":str(recordId),
        "clientRequest": {
        "resourceExpiredHour": 24,
        "scene": 0
        }
        })
        headers = {
            'Authorization': 'basic {}'.format(os.environ.get("CREDS")),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        body = response.json()

        if not response.status_code==200:
            print("****************************************",body)

        

       # starting the recording!!!

        url = "https://api.agora.io/v1/apps/{}/cloud_recording/resourceid/{}/mode/individual/start".format(os.environ.get("APPID"),body["resourceId"])

        payload = json.dumps({
        "uid": str(recordId),
        "cname": channel,
        "clientRequest": {
            "token": token,
            "recordingConfig": {
            "channelType": 1,
            "subscribeUidGroup": 0
            },
            "snapshotConfig": {
            "captureInterval": 5,
            "fileType": ["jpg"]
            },
            "storageConfig": storageConfig(mid)
        }
        })
        headers = {
            'Authorization': 'basic {}'.format(os.environ.get("CREDS")),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
    except Exception as e:
        print(str(e))

# def queryStatus(rid,sid):
#     url = "https://api.agora.io/v1/apps/{}/cloud_recording/resourceid/{}/sid/{}/mode/individual/query".format(os.environ.get("APPID"),rid,sid)
#     payload={}
#     headers = {
#             'Authorization': 'basic {}'.format(os.environ.get("CREDS"))
#         }

#     response = requests.request("GET", url, headers=headers, data=payload)
#     data = response.json()
#     return data["code"]
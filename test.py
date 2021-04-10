import boto3

import time
from dotenv import load_dotenv
load_dotenv()
import os

s3 = boto3.resource(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
)




# for bucket in s3.buckets.all():
#     for obj in bucket.objects.filter(Prefix='directory1/'):
#         # print('{}'.format(obj.key))
#         a = obj.key.split('__uid_s_')[1].split('__uid_e_video_')[0]
#         print(a)


# FOR SAVING IMAGE
# name = 'image/image'+str(time.time())
# s3.Bucket('emotionly').download_file("directory1/directory2/1cd3d60b784382f12ce30fa615421852_uwb-lIl-ZXZ__uid_s_2725317129__uid_e_video_20210409165541285.jpg",name)
# os.remove(name)


"""
s3 bucket -> ['directoryname/filename']
loop throug the keys:
    if key.startswith('{}/'.format(mid))
        #if first time yes! then create a folder with this mid!!!
        if key.regex(''.format()):
            #create a folder for mid locally! if its first time encountering the user!


        save the result to db
        delete the folder with this uid
    delete the folder with this mid


"""



from flask import Flask
from db import db
import os,schedule
from dotenv import load_dotenv
from flask_cors import CORS
# from celeryConfig import make_celery
load_dotenv()
app = Flask(__name__)
CORS(app)




app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("ADBURL") if os.environ.get("DEPLOYED")=='True' else os.environ.get("LDBURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
# app.config['CELERY_BROKER_URL']=os.environ.get('CELERY_BROKER_URL')
# app.config['CELERY_RESULT_BACKEND']=os.environ.get('CELERY_RESULT_BACKEND')
print(app.config['SQLALCHEMY_DATABASE_URI'])
# client= make_celery(app)




db.init_app(app)

# @app.before_first_request
# def runThis():
#     db.create_all()

    # blueprint for auth routes in our app
from routes.user import user as user_blueprint
app.register_blueprint(user_blueprint)

from routes.meeting import meeting as meeting_blueprint
app.register_blueprint(meeting_blueprint)

if __name__=="__main__":
    if os.environ.get("DEPLOYED")=='True':
        app.run(port=8000,host="0.0.0.0",debug=True)
    else:
        app.run(port=5000,debug=True)




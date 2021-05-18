import os


if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import traceback
import uvicorn
from fastapi import FastAPI
from flask import Flask, request, Response, render_template
from flask_cors import CORS
from lotify.client import Client

from fastapi.middleware.wsgi import WSGIMiddleware

from models.database import db, engine, Base, SessionLocal

from controller import line_controller
from controller.liff_controller import liff_share_controller

app = FastAPI()

app.include_router(line_controller.router)


flask_app = Flask(__name__)
CORS(flask_app)

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(flask_app)
with flask_app.app_context():
    db.create_all()

# api = Api(flask_app)

# api.add_resource(LineController, '/webhooks/line')


@flask_app.errorhandler(500)
def internal_error(e):
    error_trace = str(traceback.format_exc())[-300:]
    msg = 'P+ bot: url: ' + str(request.url) + \
          " inbound: " + str(request.remote_addr) + " log: " + error_trace
    lotify = Client()
    lotify.send_message(access_token=os.getenv('LINE_NOTIFY_TOKEN'), message=msg)
    return "500"


@flask_app.route("/health", methods=['GET'])
def health_check():
    return 'ok'


@flask_app.route("/liff/share", methods=['GET'])
def liff_page():
    flex, liff_id = liff_share_controller()

    if flex and liff_id:
        return Response(render_template('share_message.html', flex=flex, liff_id=liff_id))
    else:
        return Response(render_template('liff_redirect.html', liff_id=liff_id))



app.mount("/", WSGIMiddleware(flask_app))

if __name__ == '__main__':
    uvicorn.run("api:app", host='0.0.0.0', port=5000, reload=True)

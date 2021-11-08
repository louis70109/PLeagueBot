import os

if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import uvicorn
from fastapi import FastAPI
from flask import Flask, Response, render_template
from flask_cors import CORS
from fastapi.middleware.wsgi import WSGIMiddleware
from sqlalchemy import create_engine
from models.database import Base
import models.database as db

from controller import line_controller
from controller.liff_controller import liff_share_controller

app = FastAPI()

flask_app = Flask(__name__)
CORS(flask_app)


@app.on_event("startup")
async def startup():
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


app.include_router(line_controller.router)


@app.get("/")
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
    uvicorn.run("api:app", host='0.0.0.0', port=5000)

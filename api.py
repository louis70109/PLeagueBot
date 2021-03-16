import os
import traceback

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from lotify.client import Client

from models.database import db

if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

from controller.line_controller import LineController
from controller.liff_controller import LiffController

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)

api.add_resource(LineController, '/webhooks/line')
api.add_resource(LiffController, '/liff/share')


@app.errorhandler(500)
def internal_error(e):
    error_trace = str(traceback.format_exc())[-300:]
    msg = 'P+ bot: url: ' + str(request.url) + " inbound: " + str(request.remote_addr) + " log: " + error_trace
    lotify = Client()
    lotify.send_message(access_token=os.getenv('LINE_NOTIFY_TOKEN'), message=msg)
    return "500"


@app.route("/health", methods=['GET'])
def health_check():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

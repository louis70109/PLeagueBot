from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv


load_dotenv()

from controller.line_controller import LineController
from controller.liff_controller import LiffController

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(LineController, '/webhooks/line')
api.add_resource(LiffController, '/liff/share')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

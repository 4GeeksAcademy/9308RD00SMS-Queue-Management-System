"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from utils import APIException, generate_sitemap
from admin import setup_admin
from flask_cors import CORS
from database import Queue
from models import db, User
from sms import send

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



list_of_persons = Queue()

@app.route('/new/people', methods=['POST'])
def create_people():
    person = request.json
    list_of_persons.enqueue(person)
    send("hello you added to the queue", person["phone_number"])
    return jsonify(list_of_persons.get_queue())




@app.route('/peoples', methods=['GET'])
def get_all():
    Queue = list_of_persons.get_queue()
    return jsonify(Queue), 200
    


@app.route('/people', methods=['GET'])
def next_inline():
    next = list_of_persons.dequeue()
    return jsonify(next), 200



#@app.route('/members/<int:member_id>', methods=['DELETE'])
#def remove_member(member_id):
 #   jackson_family.delete_member(member_id)
  #  return jsonify(jackson_family.get_all_members())


















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

from flask import Flask
from . import write_detail

app = Flask(__name__)

app.register_blueprint(write_detail.blue_write)
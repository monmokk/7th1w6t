from flask import Flask
from . import write

app = Flask(__name__)

app.register_blueprint(write.blue_write)
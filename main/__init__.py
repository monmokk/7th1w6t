from flask import Flask
from . import write
from . import login
from . import main_listing



app = Flask(__name__)

app.register_blueprint(write.blue_write)
app.register_blueprint(login.blue_login)
app.register_blueprint(main_listing.blue_main)

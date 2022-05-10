from flask import Flask
<<<<<<< HEAD
from . import write
=======
from . import login
from . import write_detail
from . import main_listing
>>>>>>> login



app = Flask(__name__)

<<<<<<< HEAD
app.register_blueprint(write.blue_write)
=======
app.register_blueprint(login.blue_login)
app.register_blueprint(write_detail.blue_write)
app.register_blueprint(main_listing.blue_main)
>>>>>>> login

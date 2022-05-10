from flask import Flask, render_template, request, jsonify, Blueprint

blue_write = Blueprint("write_detail", __name__, template_folder='templates')

@blue_write.route("/write")
def write_detail():
    return render_template('write.html')
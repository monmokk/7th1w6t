from flask import Flask, render_template, request, jsonify, Blueprint, redirect, url_for
import jwt

blue_main = Blueprint("main_listing", __name__, template_folder='templates')

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.t0nrj.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SPARTA'

@blue_main.route("/main")
def main_listing():
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('main.html')
    except Exception as e:
        return redirect(url_for("login.login"))


@blue_main.route('/listing', methods=['GET'])
def show_main():
    dog_lists = list(db.dog.find({}, {'_id': False}))
    return jsonify({'all_lists': dog_lists})
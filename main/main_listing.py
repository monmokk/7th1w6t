from flask import Flask, render_template, request, jsonify, Blueprint

blue_main = Blueprint("main_listing", __name__, template_folder='templates')

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.t0nrj.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@blue_main.route("/main")
def main():
    return render_template('main.html')

@blue_main.route("/main", methods=['GET'])
def main_listing():
    dog_lists = list(db.dog.find({},{'_id':False}))
    return jsonify({'all_lists': dog_lists})




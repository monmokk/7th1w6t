from flask import Flask, render_template, request, jsonify, Blueprint

blue_main = Blueprint("main_listing", __name__, template_folder='templates')

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.t0nrj.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

@blue_main.route("/main")
def main_listing():
    dog_lists = list(db.dog.find({},{'_id':False}))

    print(dog_lists)
    return render_template('main.html', dog_list=dog_lists)


@blue_main.route('/listing', methods=['GET'])
def show_main():
    return jsonify({'all_lists': dog_lists})

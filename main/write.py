from datetime import datetime

from bs4 import BeautifulSoup
import requests

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.t0nrj.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
import jwt

blue_write = Blueprint("write", __name__, template_folder='templates', url_prefix='/write')
SECRET_KEY = 'SPARTA'

@blue_write.route('/')
def home():
    try:
        print("dsadasdadadasdadas", request)
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('write.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login.login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login.login"))
    except Exception :
        return redirect(url_for("login.login"))

@blue_write.route("/write")
def write():
    return render_template('write.html')


@blue_write.route("/write/<idx>")
def detailPage(idx):
    try:
        idx = int(idx)
        dogInfo = list(db.dog.find({'idx':idx}))
    except Exception as e :
        print(e)
    return render_template('write.html', dogInfo=dogInfo)

@blue_write.route('/writing', methods=['GET'])
def writing():
    dogTypeList = list(findDogType())
    return jsonify({'dogTypes':dogTypeList})

@blue_write.route('/posting', methods=['POST'])
def posting():
    file = request.files["file_give"]
    name_receive = request.form["name_give"]
    age_receive = request.form["age_give"]
    dogType_receive = request.form["dogType_give"]
    character_receive = request.form["character_give"]
    fromLocation_receive = request.form["fromLocation_give"]
    toLocation_receive = request.form["toLocation_give"]
    withDog_receive = request.form["withDog_give"]
    withKids_receive = request.form["withKids_give"]
    explain_receive = request.form["explain_give"]

    extension = file.filename.split('.')[-1]
    today = datetime.now()
    my_time = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{my_time}'
    save_to = f'main/static/{filename}.{extension}'
    file.save(save_to)

    idx = len(list(db.dog.find())) + 1

    doc = {
        'idx' : idx,
        'file':f'{filename}.{extension}',
        'name':name_receive,
        'age':age_receive ,
        'dogType':dogType_receive,
        'character':character_receive,
        'fromLocation':fromLocation_receive,
        'toLocation':toLocation_receive,
        'withDog':withDog_receive,
        'withKids':withKids_receive,
        'explain':explain_receive
    }
    db.dog.insert_one(doc)

    return jsonify({'msg' : f'"{name_receive}" 정보 등록완료'})

def findDogType():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    page = "https://namu.wiki/w/견종"
    data = requests.get(page, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    contents = soup.find_all("ul", {"class": "ss2SqVXG"})
    dogTypeList = list()

    for content in contents:
        dogTypes = content.find_all("div", {"class": "-Fv-UxxF"})
        for dogType in dogTypes:
            if dogType.text.find(":") != -1:
                break
            else:
                dogTypeList.append(dogType.text)
    return dogTypeList
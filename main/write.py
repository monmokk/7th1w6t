from datetime import datetime
import jwt
from bs4 import BeautifulSoup
import requests

from pymongo import MongoClient

client = MongoClient('')
db = client.dbsparta

from flask import Flask, render_template, request, jsonify, Blueprint, url_for, redirect

blue_write = Blueprint("write", __name__, template_folder='templates')

SECRET_KEY = 'SPARTA'


@blue_write.route("/write")
def write():

    return render_template('write.html')



@blue_write.route("/write/<idx>")
def detailPage(idx):
    idx = int(idx)
    try:
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        dogInfo = list(db.dog.find({'idx': idx}))
        written_usr = False
        if dogInfo[0]['insertId'] == payload['id']:
            written_usr = True
        # if dogInfo == []:
        #     dogInfo
        return render_template('write.html', dogInfo=dogInfo, written_usr=written_usr, loginId=payload['id'])
    except Exception as e:
        print("요기가 문제개", e)
        return redirect(url_for("main_listing.main_listing"))



@blue_write.route('/writing', methods=['GET'])
def writing():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    dogTypeList = list()
    dogTypeList.append(payload['id'])
    for dogT in db.dogType.find():
        dogTypeList.append(dogT['name'])
    return jsonify({'dogTypes': dogTypeList})

@blue_write.route('/deleting', methods=['POST'])
def deleting():
    idx_receive = request.form['idx_give']

    db.dog.delete_one({'idx':int(idx_receive)})

    return redirect(url_for("login.login"))

ㄴ
@blue_write.route('/updating', methods=['POST'])
def updating():
    id_receive = request.form["id_give"]
    idx_receive = request.form["idx_give"]
    name_receive = request.form["name_give"]
    age_receive = request.form["age_give"]
    dogType_receive = request.form["dogType_give"]
    character_receive = request.form["character_give"]
    fromLocation_receive = request.form["fromLocation_give"]
    toLocation_receive = request.form["toLocation_give"]
    withDog_receive = request.form["withDog_give"]
    withKids_receive = request.form["withKids_give"]
    explain_receive = request.form["explain_give"]


    try:
        file = request.files["file_give"]
        extension = file.filename.split('.')[-1]
        today = datetime.now()
        my_time = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'file-{my_time}'
        save_to = f'main/static/{filename}.{extension}'

        fileN = f'{filename}.{extension}'
        file.save(save_to)
    except KeyError:
        file = request.form["file_give"]
        fileN = file
    except Exception as e:
        print(e)

    doc = {
        'idx': int(idx_receive),
        'file': fileN,
        'name': name_receive,
        'age': age_receive,
        'dogType': dogType_receive,
        'character': character_receive,
        'fromLocation': fromLocation_receive,
        'toLocation': toLocation_receive,
        'withDog': withDog_receive,
        'withKids': withKids_receive,
        'explain': explain_receive,
        'insertId': id_receive
    }

    db.dog.replace_one({'idx':int(idx_receive)}, doc)

    return jsonify({'msg': f'"{name_receive}" 정보 수정완료'})


@blue_write.route('/posting', methods=['POST'])
def posting():
    try:
        file = request.files["file_give"]
    except Exception as e:
        print(e)
    id_receive = request.form["id_give"]
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
        'insertId': id_receive,
        'idx': idx,
        'file': f'{filename}.{extension}',
        'name': name_receive,
        'age': age_receive,
        'dogType': dogType_receive,
        'character': character_receive,
        'fromLocation': fromLocation_receive,
        'toLocation': toLocation_receive,
        'withDog': withDog_receive,
        'withKids': withKids_receive,
        'explain': explain_receive
    }
    db.dog.insert_one(doc)

    return jsonify({'msg': f'"{name_receive}" 정보 등록완료'})



# def findDogType():
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     page = "https://namu.wiki/w/견종"
#     data = requests.get(page, headers=headers)
#     soup = BeautifulSoup(data.text, "html.parser")
#     contents = soup.find_all("ul", {"class": "ss2SqVXG"})
#     print(soup)
#     dogTypeList = list()
#
#     for content in contents:
#         dogTypes = content.find_all("div", {"class": "-Fv-UxxF"})
#         for dogType in dogTypes:
#             if dogType.text.find(":") != -1:
#                 break
#             else:
#                 # db.dogType.insert_one({'name':dogType.text})
#     return dogTypeList


for dd in db.dog.find():
    print(dd)
from flask import Flask, render_template, request
from werkzeug import secure_filename
import json
import datetime
import databaseManager

db = databaseManager.DatabaseManager('localhost','root','!Dasom0129','shs')

import requests as rq
app = Flask(__name__)


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':

        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/board/SelectBoard', methods=['POST', 'GET'])
def SelectBoard():
    li = []
    data = db.executeQuery2("select * from board")
    for id, name, type in data:
        dic = {}
        dic['id'] = id
        dic['name'] = name
        dic['type'] = type
        li.append(dic)
    return json.dumps(li, ensure_ascii=False)

@app.route('/board/SelectWriting', methods=['POST', 'GET'])
def SelectWriting():
    li = []
    board_id = None
    if request.method == 'POST':
        board_id = request.form['board_id']
    else:
        board_id = request.args.get('board_id')
    data = db.executeQuery("select * from writing where board_id = %s and `show` = 1", board_id)
    for id, title, writer, content ,update_time ,write_time,view,show,board_id in data:
        dic = {}
        dic['id'] = id
        dic['title'] = title
        dic['writer'] = writer
        dic['content'] = content
        dic['update_time'] = datetime.datetime.strftime(update_time,   "%Y-%m-%d %H:%M:%S")
        dic['write_time'] =  datetime.datetime.strftime(write_time,   "%Y-%m-%d %H:%M:%S")
        dic['view'] = view
        dic['show'] = show
        dic['board_id'] = board_id
        li.append(dic)
    return json.dumps(li, ensure_ascii=False)

@app.route('/board/SelectClient', methods=['POST', 'GET'])
def SelectClient():
    if request.method == 'POST':
        id = request.form['id']
    else:
        id = request.args.get('id')
    data = db.executeQuery("select * from client where id = %s", id)
    for id, password, name, type ,ho_id ,ho_dong_id in data:
        dic = {}
        dic['id'] = id
        dic['password'] = password
        dic['name'] = name
        dic['type'] = type
        dic['ho_id'] = ho_id
        dic['ho_dong_id'] = ho_dong_id
    return json.dumps(dic, ensure_ascii=False)


@app.route('/board/SendWriting', methods=['POST', 'GET'])
def SendWriting():
    dic = {}
    if request.method == 'POST':
        title = request.form['title']
        writer=request.form['writer']
        content=request.form['content']
        board_id=request.form['board_id']
    else:
        title = request.args.get('title')
        writer= request.args.get('writer')
        content= request.args.get('content')
        board_id= request.args.get('board_id')


    db.updateQuery("insert into writing  (title, writer ,content , board_id) values(%s,%s,%s,%s)",
                         (title,writer,content,board_id))
    return 'sucess'

@app.route('/board/SelectWritingOne', methods=['POST', 'GET'])
def SelectWritingOne():
    li=[]
    if request.method == 'POST':
        id = request.form['id']
    else:
        id = request.args.get('id')
    data = db.executeQuery("select * from writing where id = %s", id)
    for id, title, writer, content, update_time, write_time, view, show, board_id in data:
        dic = {}
        dic['id'] = id
        dic['title'] = title
        dic['writer'] = writer
        dic['content'] = content
        dic['update_time'] = datetime.datetime.strftime(update_time, "%Y-%m-%d %H:%M:%S")
        dic['write_time'] = datetime.datetime.strftime(write_time, "%Y-%m-%d %H:%M:%S")
        dic['view'] = view
        dic['show'] = show
        dic['board_id'] = board_id
        li.append(dic)
    return json.dumps(dic, ensure_ascii=False)


@app.route('/board/SendWritingModify', methods=['POST', 'GET'])
def sendWritingModify():
    if request.method == 'POST':
        title = request.form['title']
        content=request.form['content']
        id=request.form['id']
    else:
        title = request.args.get('title')
        content= request.args.get('content')
        id=request.args.get('id')

    db.updateQuery("update `writing` SET title=%s, content=%s, `update_time`=now() where id=%s",(title,content,id))

    return 'sucess'

@app.route('/board/DeleteWriitngOne', methods=['POST', 'GET'])
def deleteWritingOne():
    show_int=int(1)
    if request.method == 'POST':
        id=request.form['id']
    else:
        id=request.args.get('id')

    db.updateQuery("update `writing` SET `show`=0  where id=%s", (id))
    return 'sucess'



@app.route('/board/SendComment', methods=['POST', 'GET'])
def sendComment():
    if request.method == 'POST':
        writer = request.form['writer']
        content=request.form['content']
        writing_id=request.form['writing_id']
    else:
        writer = request.args.get('writer')
        content= request.args.get('content')
        writing_id= request.args.get('writing_id')

    db.updateQuery("insert into `comment`(writer, content ,writing_id) values(%s,%s,%s)",
                         (writer,content,writing_id))
    return 'sucess'


@app.route('/board/SelectComment', methods=['POST', 'GET'])
def selectComment():
    li = []
    writing_id = None
    if request.method == 'POST':
        writing_id = request.form['writing_id']
    else:
        writing_id = request.args.get('writing_id')
    data = db.executeQuery("select * from `comment` where `writing_id` = %s and `show` = 1", writing_id)
    for id, writer, content, update_time ,write_time,show,reply,writing_id in data:
        dic = {}
        dic['id'] = id
        dic['writer'] = writer
        dic['content'] = content
        dic['update_time'] = datetime.datetime.strftime(update_time,   "%Y-%m-%d %H:%M:%S")
        dic['write_time'] =  datetime.datetime.strftime(write_time,   "%Y-%m-%d %H:%M:%S")
        dic['show'] = show
        dic['reply']=reply
        dic['writing_id'] = writing_id
        li.append(dic)
    return json.dumps(li, ensure_ascii=False)

@app.route('/board/SelectCommentCount', methods=['POST', 'GET'])
def selectCommentCount():
    writing_id = None
    if request.method == 'POST':
        writing_id = request.form['writing_id']
    else:
        writing_id = request.args.get('writing_id')
    data = db.executeQuery("select count(*) from `comment` where `writing_id` = %s and `show` = 1", writing_id)
    for count in data:
        dic = {}
        dic['count'] = count[0]
    return json.dumps(dic, ensure_ascii=False)


@app.route('/board/DeleteComment', methods=['POST', 'GET'])
def deleteComment():
    show_int=int(1)
    if request.method == 'POST':
        id=request.form['id']
    else:
        id=request.args.get('id')

    db.updateQuery("update `comment` SET `show`=0  where id=%s", (id))
    return 'sucess'

@app.route('/board/ModifyComment', methods=['POST', 'GET'])
def modifyComment():
    if request.method == 'POST':
        content=request.form['content']
        id=request.form['id']
    else:
        content= request.args.get('content')
        id = request.args.get('id')

    db.updateQuery("update `comment` SET  `content`=%s, `update_time`=now() where id=%s", (content, id))

    return 'sucess'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
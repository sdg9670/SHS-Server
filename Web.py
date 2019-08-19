from flask import Flask, request
import json
import datetime
import databaseManager
from pyfcm import FCMNotification

db = databaseManager.DatabaseManager('localhost', 'root', '!Dasom0129', 'shs')
push_service = FCMNotification(
    api_key="AAAAXE7sxxA:APA91bGJVD6TxWf_9WBZS97vToJ18SG-OnslG8g-crwm1WjJxPVa9gBvPFm3C4ma0lpHuOZuLOepeOPftXA4DmBQjcsejFFKjt2rFarqpdk8zNm2oay-JCLpu5N_bAWezdSKYGUP8RD1")
app = Flask(__name__)


def json_default(value):
    if isinstance(value, (datetime.datetime)):
        return value.__str__()

@app.route('/doorlock_image', methods=['GET'])
def GetDoorLockImage():
    dong = request.args.get('dong')
    ho = request.args.get('ho')
    data = None
    data = db.executeQuery("select * from doorlock_image where dong = %s and ho = %s order by id desc", (dong, ho))
    print(str(json.dumps(data, ensure_ascii=False, default=json_default)))
    return json.dumps(data, ensure_ascii=False, default=json_default)

@app.route('/window', methods=['GET'])
def SelectWindow():
   data = db.executeQuery2("select `window`.*, `client`.`name` from `window`, `client` where `client`.id = `window`.id;")
   return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/curtain', methods=['PUT'])
def putCurtain():
   print(request.json)
   lux_over = request.json['lux_over']
   lux_set = request.json['lux_set']
   id = request.json['id']
   db.updateQuery("update `curtain` SET lux_set=%s, lux_over=%s where id=%s",
                  (lux_set,lux_over,id))
   return 'sucess'

@app.route('/window', methods=['PUT'])
def putWindow():
   print(request.json)
   temp_over = request.json['temp_over']
   temp_set = request.json['temp_set']
   humi_over = request.json['humi_over']
   humi_set = request.json['humi_set']
   rain_over = request.json['rain_over']
   rain_set = request.json['rain_set']
   dust_over = request.json['dust_over']
   dust_set = request.json['dust_set']
   id = request.json['id']
   db.updateQuery("update `window` SET temp_set=%s, temp_over=%s, humi_set=%s, humi_over=%s, rain_set=%s, rain_over=%s, dust_set=%s, dust_over=%s where id=%s",
                  (temp_set,temp_over,humi_set,humi_over,rain_set,rain_over,dust_set,dust_over,id))
   return 'sucess'

@app.route('/curtain', methods=['GET'])
def SelectCurtain():
   data = db.executeQuery2("select `curtain`.*, `client`.`name` from `curtain`, `client` where `client`.id = `curtain`.id;")
   return json.dumps(data, ensure_ascii=False, default=json_default)

@app.route('/sensor', methods=['GET'])
def SelectSensor():
   data = db.executeQuery2("select * from sensor")
   return json.dumps(data, ensure_ascii=False, default=json_default)

'''========================================='''

'''친구 요청 목록'''


@app.route('/requestFriend', methods=['GET'])
def GetRequestFriend():
    id = request.args.get('id')

    data = db.executeQuery("select c.id, c.someid as clientid, c.clientid as someid, c.newmsg, " +
                           "cli.name as somename, cli.dong as somedong, cli.ho as someho, cli.id_name as someidname " +
                           "from contact c inner join `client` cli on cli.id = c.clientid " +
                           "left join contact d on d.clientid = c.someid and d.someid = c.clientid " +
                           "where c.someid = %s and d.id is null", (id,))
    return json.dumps(data, ensure_ascii=False, default=json_default)


'''친구 요청 거절'''


@app.route('/requestFriend', methods=['DELETE'])
def DeleteRequestFriend():
    clientid = request.args.get('clientid')
    someid = request.args.get('someid')
    db.updateQuery("delete from contact where clientid = %s and someid = %s", (someid, clientid))
    return 'sucess'


'''친구 목록'''


@app.route('/friend', methods=['GET'])
def GetFriend():
    id = request.args.get('id')
    data = db.executeQuery(
        "select c.*, cli.name as somename, cli.dong as somedong, cli.ho as someho, cli.id_name as someidname " +
        "from contact c inner join `client` cli on cli.id = c.someid " +
        "inner join contact d on c.clientid = d.someid " +
        "where c.clientid = %s and d.clientid = c.someid", (id,))
    return json.dumps(data, ensure_ascii=False, default=json_default)


'''이미 등록된 친구인지 확인'''


@app.route('/friendCheck', methods=['GET'])
def friendCheck():
    clientid = request.args.get('clientid')
    someidname = request.args.get('someidname')
    data = db.executeQuery("select *" +
                           "from contact where clientid = %s and someid = (select id from `client` where `id_name` = %s)",
                           (clientid, someidname))
    return json.dumps(data, ensure_ascii=False, default=json_default)


'''친구 수락 및 요청'''


@app.route('/friend', methods=['POST'])
def PostFriend():
    clientid = request.json['clientid']
    someidname = request.json['someidname']
    db.updateQuery("insert into contact(clientid, someid) values(%s, (select id from `client` where `id_name` = %s))",
                   (clientid, someidname))
    return 'sucess'


'''친구삭제'''


@app.route('/friend', methods=['DELETE'])
def DeleteFriend():
    clientid = request.args.get('clientid')
    someid = request.args.get('someid')
    db.updateQuery("delete from contact where clientid = %s and someid = %s or clientid = %s and someid = %s",
                   (clientid, someid, someid, clientid))
    return 'sucess'


'''존재하는 친구인지 확인'''


@app.route('/friendCheck2', methods=['GET'])
def friendCheck2():
    someidname = request.args.get('someidname')
    data = db.executeQuery("select * from client where id_name = %s", (someidname,))
    return json.dumps(data, ensure_ascii=False, default=json_default)



'''===================================================================================================================='''

@app.route('/speaker', methods=['GET'])
def GetSpeaker():
   dong = request.args.get('dong')
   ho = request.args.get('ho')
   data = None
   data = db.executeQuery("select* from client where dong = %s and ho = %s and type=1", (dong, ho))
   return json.dumps(data, ensure_ascii=False, default=json_default)

@app.route('/sendfcm_ho_dong', methods=['POST'])
def sendFCM_Ho_sDong():
    print(str(request))
    title = request.json['title']
    message = request.json['message']
    ho = request.json['ho']
    dong = request.json['dong']
    data = db.executeQuery("SELECT fcm FROM client WHERE ho = %s and dong = %s", (ho, dong,))
    data2 = []
    for i in data:
        if i['fcm'] != None:
            data2.append(i['fcm'])
    result = push_service.notify_multiple_devices(registration_ids=data2, message_title=title, message_body=message)
    return 'sucess'


@app.route('/sendfcm_dong', methods=['POST'])
def sendFCM_Dong():
    print(str(request))
    title = request.json['title']
    message = request.json['message']
    dong = request.json['dong']
    data = db.executeQuery("SELECT fcm FROM client WHERE dong = %s", (dong,))
    data2 = []
    for i in data:
        if i['fcm'] != None:
            data2.append(i['fcm'])
    result = push_service.notify_multiple_devices(registration_ids=data2, message_title=title, message_body=message)
    return str(data2)
    return 'sucess'


@app.route('/sendfcm', methods=['POST'])
def sendFCM():
    client_id = request.json['client_id']
    title = request.json['title']
    message = request.json['message']
    data = db.executeQuery("SELECT fcm FROM client WHERE client = %s", (client_id,))

    result = push_service.notify_single_device(registration_id=data[0]['fcm'], message_title=title,
                                               message_body=message)
    return str(data[0]['fcm'])


@app.route('/board', methods=['GET'])
def SelectBoard():
    data = db.executeQuery2("select * from board")
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/client', methods=['GET'])
def SelectClient():
    id = request.args.get('id')
    data = db.executeQuery("select * from client where id = %s", id)
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/client', methods=['PUT'])
def SelectClientModify():
    fcm = request.args.get('fcm')
    id = request.args.get('id')
    db.updateQuery("update `client` SET fcm=%s where id=%s", (fcm, id))
    return 'success'


@app.route('/writing', methods=['POST'])
def PostWritibng():
    title = request.json['title']
    writer = request.json['writer']
    content = request.json['content']
    board_id = request.json['board_id']
    data = {}
    db.updateQuery("insert into writing  (title, writer ,content , board_id) values(%s,%s,%s,%s)",
                   (title, writer, content, board_id))
    return "sucess"


@app.route('/last_writing', methods=['GET'])
def GetLast_writing():
    data = db.executeQuery2("SELECT * FROM writing order by id desc limit 1")
    print(data)
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/writing', methods=['GET'])
def GetWriting():
    board_id = request.args.get('board_id')
    id = request.args.get('id')
    data = None
    if id is not None:
        data = db.executeQuery(
            "SELECT writing.*, (SELECT COUNT(*) FROM comment WHERE writing_id=writing.id AND `show` = 1) AS comment_count, (SELECT name FROM client WHERE id=writing.writer) AS writer_name from writing where id = %s and `show` = 1 order by id desc",
            id)
    else:
        data = db.executeQuery(
            "SELECT writing.*, (SELECT COUNT(*) FROM comment WHERE writing_id=writing.id AND `show` = 1) AS comment_count, (SELECT name FROM client WHERE id=writing.writer) AS writer_name from writing where board_id = %s and `show` = 1 order by id desc",
            board_id)
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/writing', methods=['PUT'])
def sendWritingModify():
    print(request.get_json())
    title = request.json['title']
    content = request.json['content']
    id = request.json['id']
    db.updateQuery("update `writing` SET title=%s, content=%s, `update_time`=now() where id=%s", (title, content, id))
    return 'sucess'


@app.route('/writing', methods=['DELETE'])
def deleteWritingOne():
    id = request.args.get('id')
    db.updateQuery("update `writing` SET `show`=0  where id=%s", (id))
    return 'sucess'


@app.route('/comment', methods=['POST'])
def postComment():
    writer = request.json['writer']
    content = request.json['content']
    writing_id = request.json['writing_id']
    db.updateQuery("insert into `comment`(writer, content ,writing_id) values(%s,%s,%s)",
                   (writer, content, writing_id))
    data = db.executeQuery("SELECT fcm FROM client WHERE id = (Select writer from writing where id=%s)", (writing_id,))
    result = push_service.notify_single_device(registration_id=data[0]['fcm'], message_title="댓글 알림", message_body=str(content))
    return 'sucess'


@app.route('/comment', methods=['GET'])
def getComment():
    writing_id = request.args.get('writing_id')
    data = db.executeQuery(
        "select *, (SELECT name FROM client WHERE id=comment.writer) AS writer_name from `comment` where `writing_id` = %s and `show` = 1",
        writing_id)
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/comment', methods=['DELETE'])
def deleteComment():
    id = request.args.get('id')
    db.updateQuery("update `comment` SET `show`=0  where id=%s", id)
    return 'sucess'


@app.route('/comment', methods=['PUT'])
def putComment():
    content = request.json['content']
    id = request.json['id']
    db.updateQuery("update `comment` SET  `content`=%s, `update_time`=now() where id=%s", (content, id))
    return 'sucess'


@app.route('/writing_image', methods=['POST'])
def PostWriting_Image():
    path = request.json['path']
    writing_id = request.json['writing_id']
    data = {}
    db.updateQuery("insert into writing_image  (path, writing_id) values(%s,%s)",
                   (path, writing_id))
    return "sucess"


@app.route('/writing_image_multi', methods=['POST'])
def PostWriting_Image_multi():
    jsonArray = request.json
    print("asd" + str(jsonArray))
    for i in jsonArray:
        db.updateQuery("insert into writing_image  (path, writing_id, name) values(%s,%s,%s)",
                       (i['path'], i['writing_id'], i['name']))
    return "sucess"


@app.route('/writing_image', methods=['GET'])
def GetWriting_image():
    writing_id = request.args.get('writing_id')
    data = db.executeQuery("select * from writing_image where writing_id=%s", writing_id)
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/writing_image', methods=['DELETE'])
def Delete_image():
    jsonArray = {}
    jsonArray = request.json
    print("jsonArray" + str(jsonArray))
    for i in jsonArray:
        id = str(i['id'])
        db.updateQuery("delete from writing_image where id like %s", id)
    return "sucess"


@app.route('/logincheck', methods=['GET'])
def Logincheck():
    id_name = request.args.get('id_name')
    password = request.args.get('password')
    data = None
    data = db.executeQuery("select* from client where id_name = %s and password = sha2(%s,512)", (id_name, password))
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/updatefcm', methods=['PUT'])
def UpdateFCM():
    id = request.json['id']
    fcm = request.json['fcm']
    if fcm == "널":
        db.updateQuery("update client set fcm = NULL where id = %s", (id,))
    else:
        db.updateQuery("update client set fcm = %s where id = %s", (fcm, id))
    print("" + str(id) + "fcm" + fcm)
    return "sucess"


@app.route('/writing_vote', methods=['POST'])
def postWriting_vote():
    jsonArray = request.json
    for i in jsonArray:
        db.updateQuery("insert into writing_vote  (name, writing_id) values(%s,%s)",
                       (i['name'], i['writing_id']))
    return "sucess"


@app.route('/vote_whether', methods=['POST'])
def postVote_whether():
    vote_id = request.json['vote_id']
    client_id = request.json['client_id']
    db.updateQuery("insert into vote_whether (vote_id, client_id) values(%s,%s)", (vote_id, client_id))
    return "sucess"


@app.route('/check_vote', methods=['GET'])
def check_Vote():
    writing_id = request.args.get('writing_id')
    client_id = request.args.get('client_id')
    data = db.executeQuery("select a.* from vote_whether a " +
                           "inner join writing_vote b " +
                           "on a.vote_id = b.id " +
                           "where a.client_id = %s and b.writing_id = %s", (client_id, writing_id))
    return json.dumps(data, ensure_ascii=False, default=json_default)


@app.route('/writing_vote', methods=['GET'])
def getWriting_vote():
    writing_id = request.args.get('writing_id')
    sql = "select count(*) from vote_whether where vote_id = id"
    data = db.executeQuery("select *, (" + sql + ") as amount from writing_vote where writing_id=%s", (writing_id))
    return json.dumps(data, ensure_ascii=False, default=json_default)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
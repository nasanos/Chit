from flask import Flask, render_template, session, request, url_for, send_from_directory, redirect
from flask_socketio import SocketIO, emit
from werkzeug.security import check_password_hash
import sqlalchemy, json
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabledefs import *

app = Flask(__name__, static_url_path="")
app.secret_key = "SECRET_KEY"
app.debug = True

socketio = SocketIO(app)
sql_eng = sqlalchemy.create_engine("sqlite:///database/log.db", echo=True)

#Pages
@app.route("/")
def index():
    if not session.get("logged"):
        return render_template("logon.html")
    else:
        Sess = sessionmaker(bind=sql_eng)
        sesh = Sess()
        usrlist = []
        for usr in sesh.query(User.username):
            usrlist.append(usr[0])
        return render_template("index.html", username=session["username"], usrlist=json.dumps(usrlist))

#Static files
@app.route("/scripts/<filename>")
def sendscripts(filename):
    return send_from_directory("scripts/", filename)
@app.route("/styles/<filename>")
def sendstyles(filename):
    return send_from_directory("styles/", filename)
@app.route("/fonts/<filename>")
def sendfonts(filename):
    return send_from_directory("fonts/", filename)

#Sessioning
@app.route("/logon/", methods=["POST", "GET"])
def logon():
    Sess = sessionmaker(bind=sql_eng)
    sesh = Sess()
    if request.method == "POST":
        passed_username = request.form["username"]
        passed_password = request.form["password"]
    if sesh.query(User).filter(User.username.in_([passed_username])).first():
        temp_var = sesh.query(User).filter_by(username=passed_username).first()
        rslt = check_password_hash(temp_var.password, passed_password)
    else:
        rslt = False
    if rslt:
        session["logged"] = True
        session["username"] = passed_username
        now = datetime.utcnow()
        string_now = str(now.year)+str(now.month)+str(now.day)+":"+str(now.hour)+":"+str(now.minute)
        log_to_db = Loggedon(date=string_now, msg="Logon: "+passed_username)
        sesh.add(log_to_db)
        sesh.commit()
    else:
        now = datetime.utcnow()
        string_now = str(now.year)+str(now.month)+str(now.day)+":"+str(now.hour)+":"+str(now.minute)
        log_to_db = Loggedon(date=string_now, msg="Incorrect logon attempt: "+passed_username+", "+passed_password)
        sesh.add(log_to_db)
        sesh.commit()
    return redirect(url_for("index"))
@app.route("/logoff/")
def logoff():
    session["logged"] = False
    return redirect(url_for("index"))

#Connecting/disconnecting
@socketio.on("connect", namespace="/msgs")
def msgsconnect():
    print("Client connected.")
@socketio.on("disconnect", namespace="/msgs")
def msgsdisconnect():
    print("Client disconnected.")

#Messaging
@socketio.on("init_chat", namespace="/msgs")
def setup_msgs(conv_partner):
    Sess = sessionmaker(bind=sql_eng)
    sesh = Sess()
    emit("chat_clear")
    temp_var = [session["username"], conv_partner["data"]]
    temp_var.sort()
    session["conv_id"] = temp_var[0]+","+temp_var[1]
    for qconts in sesh.query(Convo).filter_by(convoid=session["conv_id"]).all():
        emit("msgpost", {"data": qconts.chatmsg, "username": qconts.username})
@socketio.on("msgevent", namespace="/msgs")
def msgsender(msg):
    Sess = sessionmaker(bind=sql_eng)
    sesh = Sess()
    now = datetime.utcnow()
    emit("msgpost", {"data": msg["data"], "username": session["username"]}, broadcast=True)
    sesh.add(Convo(convoid=session["conv_id"], chatmsg=msg["data"], timestamp=(str(now.year)+str(now.month)+str(now.day)+":"+str(now.hour)+":"+str(now.minute)), username=usname))
    sesh.commit()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")

import pickle
from flask import Flask, render_template, jsonify,request
from SqlAlchemy import load_user_details, register_user_details, get_links
import numpy as np
import pandas as pd
from Recommendation import recommendation
from Get_Url import extract_video_id

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        # print(request.form)
        
        myDict = request.form
        username = myDict['username']
        password = myDict['password']
        if load_user_details(username, password):
            return render_template('search.html', uname = username)
    return render_template('login.html')

@app.route("/registration", methods=['GET', 'POST'])
def Registration():
    if request.method == "POST":
        data = request.form
        name = data['name']
        city = data["city"]
        email = data["email"]
        uname = data["username"]
        password = data["password"]
        register_user_details(name,city,email,uname,password)
        return render_template("login.html")
    return render_template('registration.html')

@app.route("/songs", methods=['GET', 'POST'])
def Songs_list():
    data = request.form
    son = data['search']
    l = recommendation(son)
    print(l)
    video_id = []
    for i in l:
        print(i)
        x = get_links(i)
        video_id.append(extract_video_id(x[0]['link'].split("\\\\")[0]))
    y = get_links(son)
    y = extract_video_id(y[0]['link'])
    print(y)
    return render_template("index.html", lis = l, id = video_id, play = y)

@app.route("/play_song", methods=['GET', 'POST'])
def play_list():
    data = request.form
    son = data['song1']
    y = data['song_link']
    l = recommendation(son)
    video_id = []
    for i in l:
        x = get_links(i)
        x = x.split("\\\\")[0]
        video_id.append(extract_video_id(x[0]['link']))
    return render_template("index.html", lis = l, id = video_id, play = y)


if __name__ == "__main__":
     app.run(debug=True)

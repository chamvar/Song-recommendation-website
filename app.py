from flask import Flask, render_template, jsonify,request, session
import random
import pickle
from Generate_list import generate_random_music_list, recommend_pairs
from SqlAlchemy import load_user_details, register_user_details,add_fav,get_user_fav,add_group
import speedtest


app = Flask(__name__)
app.secret_key = 'key'
reco = []  # recommendation list
playes = 0
total = 0
skips = 0

# calculates the user satisfaction
def User_Satisfaction():
    global playes, total, skips 
    playes +=1
    if total>0:
        satisfaction_rate = ((total - skips) / total) * 100
        if satisfaction_rate > 0:
            print(satisfaction_rate)

# route page contains login
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        myDict = request.form
        username = myDict['username']
        password = myDict['password']       
        if load_user_details(username, password):
            songs,l = generate_random_music_list()
            fa = get_user_fav(username)
            reco = list(recommend_pairs(fa))
            session['reco'] = reco
            return render_template("app_web.html", song=l[0],song_id =songs[l[0]] ,lis=l, rec = reco, uname = username, favs = fa)
    return render_template('login.html')

# this function is for registration
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

# to display the music list
@app.route("/music_list/<username>",methods=["GET","POST"])
def music_list(username):
    songs,l = generate_random_music_list()
    fa = get_user_fav(username)
    reco = list(session.get('reco', []))
    if request.method == "POST":
        data = request.form
        music = data["music"]
        reco = list(reco)
        User_Satisfaction()
        return render_template("app_web.html", song=music,song_id =songs[music] ,lis=l, rec = reco, uname = username, favs = fa)
    else:
        return render_template("app_web.html",song="None",song_id =None,lis=l, rec = [None,None,None,None,None], uname = username, favs = fa)   
          
# this function skips to the next song
@app.route("/skip/<username>",methods=["GET","POST"])
def skip(username):
    global skips
    songs,l = generate_random_music_list()
    fa = get_user_fav(username)
    reco = list(session.get('reco', []))

    print(l,reco,fa)
    if request.method == "POST":
        reco = list(reco)
        data = request.form
        music = data["songg"]
        if music in l:
            available_list = l
        elif music in fa:
            available_list = fa
        else:
            available_list = reco
            skips+=1
        while True:
            x = random.choice(available_list)
            if x != music:
                break
        User_Satisfaction()
        return render_template("app_web.html", song=x,song_id =songs[x] ,lis=l, rec = reco, uname = username, favs = fa)
    else:
        return render_template("app_web.html",song="None",song_id =None,lis=l, rec = [None,None,None,None,None], uname = username, favs = fa)   

#  for displaying the recommendation list
@app.route("/recommend/<username>",methods=["GET","POST"])
def recommend(username):
    global total
    songs, l = generate_random_music_list()
    reco = []
    song = None
    reco = list(session.get('reco', []))
    fa = get_user_fav(username)
    if request.method == "POST":
        data = request.form
        if "recommend" in data:
            x = data["recommend"]
            reco = list(reco)
            song = x
            total += 1
            User_Satisfaction()
    song_id = songs.get(song)
    if len(fa) == 0:
        return render_template("app_web.html", song=song, song_id =song_id, lis=l, rec=[None,None,None,None,None], uname = username, favs = fa)
    
    return render_template("app_web.html", song=song, song_id =song_id, lis=l, rec=reco, uname = username, favs = fa)


# to add the song into favourites list
@app.route("/fav/<username>",methods=["GET","POST"])
def fav(username):
    songs,l = generate_random_music_list()
    fa = get_user_fav(username)
    reco = list(session.get('reco', []))
    if request.method == "POST":
        data = request.form
        music = data["fav"]
        if len(fa) == 0:
            session['reco']=list(recommend_pairs([music]))
            reco = list(session.get('reco', []))
        add_fav(username,music)
        add_group(username)
        faa = fa.copy()
        faa.append(music)
    song_id = songs.get(music)
    return render_template("app_web.html", song=music, song_id =song_id, lis=l, rec=reco, uname = username, favs = faa)

# to display the favourites item
@app.route("/favorites/<username>",methods=["GET","POST"])
def favourites(username):
    songs,l = generate_random_music_list()
    fa = get_user_fav(username)
    reco = []
    song = None
    reco = list(session.get('reco', []))
    if request.method == "POST":
        data = request.form
        if "favorite" in data:
            x = data["favorite"]
            reco = list(reco)
            song = x
            User_Satisfaction()
    song_id = songs.get(song)
    return render_template("app_web.html", song=song, song_id =song_id, lis=l, rec=reco, uname = username, favs = fa)

# To calculate the network traffic
import psutil
import time
def list_network_interfaces():
    interfaces = psutil.net_if_stats()
    print("Available network interfaces:")
    for interface, stats in interfaces.items():
        print(f"{interface}: {stats}")

@app.route("/measure_network_speed", methods=["GET"])
def network_traffic():
    inf = "Wi-Fi"
    try:
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
        net_in_1 = net_stat.bytes_recv
        net_out_1 = net_stat.bytes_sent
        time.sleep(1)
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
        net_in_2 = net_stat.bytes_recv
        net_out_2 = net_stat.bytes_sent
        net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
        net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
        return render_template(f"Current net-usage:\nIN: {net_in} MB/s, OUT: {net_out} MB/s")
    except KeyError:
        return render_template(f"Error: Network interface '{inf}' not found.")
        list_network_interfaces()


# measures the page load time
@app.route('/log_metrics', methods=['GET','POST'])
def log_metrics():

    if request.is_json:
        data = request.get_json()
        latency = data.get('latency')
        page_load_time = data.get('pageLoadTime')
        
        # Perform any other tasks you want with these metrics
        print('Latency:', latency)
        print('Page Load Time:', page_load_time)
    return f"Nothing"
        

# to run the flask application
if __name__ == "__main__":
    app.run(debug=True)
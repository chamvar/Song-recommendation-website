import pickle
from sqlalchemy import MetaData, Table, text,insert,create_engine,update
import pandas as pd
import pymysql
df = pd.read_csv("freelancer\\web_interface_song\\static\\music_list - Sheet1.csv")

# get connection from the database
engine = create_engine("mysql+pymysql://tjsrgq9tpyifphpvw9e7:pscale_pw_13xbemzh4WopcLWcJ3gHfaJtEuVPvB8LwkkRQYabeyp@aws.connect.psdb.cloud/db?charset=utf8mb4", connect_args = {
    "ssl" :{
    "ssl_ca": "/etc/ssl/cert.pem"
  }
})

# kmeans model
file2 = open("freelancer\\web_interface_song\\static\\kmeans.pkl",'rb')
kmeans = pickle.load(file2)
file2.close()

# MultiLabelBinarizer model
file2 = open("freelancer\\web_interface_song\\static\\mlb.pkl",'rb')
mlb = pickle.load(file2)
file2.close()

# checks the login details
def load_user_details(username, password):
    with engine.connect() as conn:
        result = conn.execute(text(f"select username,password from Customers where username = '{username}'"))
        result_all = result.all()
        if len(result_all) == 0:
            return False
        x = result_all[0]._asdict()
        if x["password"] != password:
            return False
        return True


# inserts the new user data
def register_user_details(name, city, email,uname, password):
    metadata = MetaData()
    cust_table = Table('Customers', metadata, autoload_with=engine)

    with engine.connect() as conn:
        stmt = insert(cust_table).values(Name = name, City = city, Email = email,username = uname, Password = password)
        result = conn.execute(stmt)
        conn.commit()


# get all song list
def get_songs():
    dic = {}
    with engine.connect() as conn:
        result = conn.execute(text(f"select song,song_id from Songs"))
        result_all = result.all()
        for r in result_all:
            dic[r[0]] = r[1]
    return dic

# add the fav song into the fav table
def add_fav(user_id, music):
    with engine.connect() as conn:
        metadata = MetaData()
        favorite = Table('fav', metadata, autoload_with=engine)
        result = conn.execute(text(f"SELECT * FROM fav WHERE username='{user_id}'"))
        result_all = result.all()
        s = set()
        for r in result_all:
            s.add(r[1])
        if music not in s:
            stmt = insert(favorite).values(username=user_id, song=music)
            result = conn.execute(stmt)
            print(67)
        else:
            print("Already added to favorites")
        conn.commit()

# fetch users favourite song
def get_user_fav(user_name):
    s = set()
    with engine.connect() as conn:
        metadata = MetaData()
        fav = Table('fav', metadata, autoload_with=engine)
        
        result = conn.execute(text(f"SELECT * FROM fav WHERE username='{user_name}'"))
        result_all = result.all()
        for r in result_all:
            s.add(r[1])
    return list(s)
        
# for inserting new songs into the Songs table
def insert_songs():
     with engine.connect() as conn:
        metadata = MetaData()
        songs_table = Table('Songs', metadata, autoload_with=engine)
        for i in range(0,len(df)):
            stmt = insert(songs_table).values(song=df['song'][i], song_id=df['id'][i])
            result = conn.execute(stmt)
        conn.commit()


# predicts the user which group he belongs to
def kmean_recommendation(music):
    music = [music]
    music = mlb.transform(music)
    n = kmeans.predict(music)
    return n

# assign the user into the group based on fav list
def add_group(username):
    with engine.connect() as conn:
        metadata = MetaData()
        result = conn.execute(text(f"select song from fav where username = '{username}'"))
        result_all = result.all()
        n = predict_user_group(list(result_all))
        n = n[0]
        my_table = Table('Customers', metadata, autoload_with=engine)
        stmt = update(my_table).where(my_table.c.username == username).values(goup=n)
        result = conn.execute(stmt)
        conn.commit()


def predict_user_group(result):
    lis = set()
    for i in result:
        lis.add(i[0])

    lis = list(lis)
    return kmean_recommendation(lis)
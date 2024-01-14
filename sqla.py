import pickle
from sqlalchemy import MetaData, Table, text,insert,create_engine,update
# from Get_Url import get_link
import pandas as pd
import pymysql
df = pd.read_csv("web_interface_song\\static\\music_list - Sheet1.csv")

engine = create_engine("mysql+pymysql://root:sai12@127.0.0.1/DB?charset=utf8mb4")

file2 = open("web_interface_song\\static\\kmeans.pkl",'rb')
kmeans = pickle.load(file2)
file2.close()

file2 = open("web_interface_song\\static\\mlb.pkl",'rb')
mlb = pickle.load(file2)
file2.close()

def load_user_details(username, password):
    with engine.connect() as conn:
        trans = conn.begin()  # Start a transaction
        try:
            result = conn.execute(text(f"SELECT username, password FROM customers WHERE username = :username"), username=username)
            row = result.fetchone()
            if row is None:
                return False
            if row.password != password:
                return False
        except Exception as e:
            trans.rollback()  # Roll back the transaction in case of an error
            raise e
        return True


def register_user_details(name, city, email, uname, password):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(
                text("INSERT INTO customers (Name, City, Email, username, Password) VALUES (:name, :city, :email, :username, :password)"),
                name=name, city=city, email=email, username=uname, password=password
            )
            conn.commit()
        except pymysql.IntegrityError:
            # Handle duplicate registration error
            trans.rollback()
            return False
        except Exception as e:
            trans.rollback()
            return False
    return True


def get_songs():
    dic = {}
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            result = conn.execute(text("SELECT song, song_id FROM Songs"))
            for row in result:
                dic[row[0]] = row[1]
            trans.commit()
        except Exception as e:
            trans.rollback()
    return dic

def add_fav(user_id, music):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            metadata = MetaData()
            favorite = Table('fav', metadata, autoload_with=engine)
            stmt = insert(favorite).values(username=user_id, song=music)
            result = conn.execute(stmt)
            trans.commit()
        except Exception as e:
            trans.rollback()


def get_user_fav(user_name):
    s = set()
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            metadata = MetaData()
            fav = Table('fav', metadata, autoload_with=engine)
            result = conn.execute(text(f"SELECT song FROM fav WHERE username='{user_name}'"))
            for row in result:
                s.add(row[0])
            trans.commit()
        except Exception as e:
            trans.rollback()
    return list(s)


def insert_songs():
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            metadata = MetaData()
            songs_table = Table('songs', metadata, autoload_with=engine)
            for i in range(51, len(df)):
                stmt = insert(songs_table).values(song=df['song'][i], song_id=df['id'][i])
                result = conn.execute(stmt)
            trans.commit()
        except Exception as e:
            trans.rollback()

def kmean_recommendation(music):
    music = [music]
    music = mlb.transform(music)
    n = kmeans.predict(music)
    return n

def add_group(username):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            metadata = MetaData()
            result = conn.execute(text(f"SELECT song FROM fav WHERE username = '{username}'"))
            songs = [row[0] for row in result.fetchall()]
            group = predict_user_group(songs)
            my_table = Table('Customers', metadata, autoload_with=engine)
            stmt = update(my_table).where(my_table.c.username == username).values(group=group)
            result = conn.execute(stmt)
            trans.commit()
        except Exception as e:
            trans.rollback()


def predict_user_group(result):
    lis = set()
    for i in result:
        lis.add(i[0])

    lis = list(lis)
    return kmean_recommendation(lis)

import sqlite3
import random
import uuid

def connect_db():
    conn = sqlite3.connect("veriler.db")
    return conn

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS kullanicilar (id TEXT PRIMARY KEY, ad TEXT, soyad TEXT, yas INTEGER, cinsiyet TEXT, kullanici_ad TEXT, email TEXT, sifre TEXT)")
    
    conn.commit()
    conn.close()

create_tables()

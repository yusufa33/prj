from flask import Flask, render_template, request, redirect, session
import sqlite3
import veritabani
import uuid

app = Flask(__name__)
app.secret_key = "xyusuf-akgucx"

@app.route("/")
def anasayfa():
    return render_template("anasayfa.html")

@app.route("/kayit")
def kayit_sayfasi():
    return render_template("kayit.html")

@app.route("/giris")
def giris_sayfasi():
    return render_template("giris.html")

@app.route("/cikis")
def cikis():
    session["ad"] = None
    session["sifre"] = None
    return redirect("/giris")

@app.route("/sitebilgi")
def site_hakkinda():
    return render_template("site_hakkinda.html")

@app.route("/bilgiler", methods=["POST"])
def kayit():
    ad = request.form["ad"]
    soyad = request.form["soyad"]
    yas = request.form["yas"]
    cinsiyet = request.form["cinsiyet"]
    kullanici_ad = request.form["kullanici_ad"]
    email = request.form["email"]
    sifre = request.form["sifre"]

    conn = veritabani.connect_db()
    cur = conn.cursor()

    user_id = str(uuid.uuid4())

    sorgu = f"SELECT * FROM kullanicilar WHERE kullanici_ad = '{kullanici_ad}'"
    kayitlar = cur.execute(sorgu).fetchall()

    if len(kayitlar) == 0:
        sorgu = f"INSERT INTO kullanicilar (id, ad, soyad, yas, cinsiyet, kullanici_ad, email, sifre) VALUES ('{user_id}', '{ad}', '{soyad}', {yas}, '{cinsiyet}', '{kullanici_ad}', '{email}', '{sifre}')"
        cur.execute(sorgu)
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        return render_template("kayit.html", hata="Bu kullanıcı adı zaten kayıtlı.")

@app.route("/girisbilgileri", methods=["POST"])
def giris_kontrol():
    kullanici_ad = request.form["kullanici_ad"]
    sifre = request.form["sifre"]

    conn = veritabani.connect_db()
    cur = conn.cursor()

    sorgu = f"SELECT * FROM kullanicilar WHERE kullanici_ad = '{kullanici_ad}' AND sifre = '{sifre}'"
    kayitlar = cur.execute(sorgu).fetchall()

    if len(kayitlar) == 0:
        return render_template("giris.html", hata="Kullanıcı bilgileri hatalı!")
    else:
        session["ad"] = kullanici_ad
        session["sifre"] = sifre
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

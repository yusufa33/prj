from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "xyusuf-akgucx"

def db_kayit(sorgu, fetch_tipi="one", veri=None):
    baglanti = sqlite3.connect("veriler.db")
    imlec = baglanti.cursor()

    if veri:
        imlec.execute(sorgu, veri)
    else:
        imlec.execute(sorgu)
    
    if fetch_tipi == "one":
        kayit = imlec.fetchone()
    elif fetch_tipi == "all":
        kayit = imlec.fetchall()
    else:
        kayit = None
    
    baglanti.commit()
    baglanti.close()
    return kayit

@app.route("/") 
def anasayfa():
    if "ad" in session and session["ad"] != None:         
         return render_template("index.html")
    else:
         return render_template("giris.html")

@app.route("/kayit", methods=["GET", "POST"]) 
def kayit_sayfasi():
    if request.method == "GET":
        return render_template("kayit.html")
    elif request.method == "POST":
        isim = request.form["isim"]
        soyad = request.form["soyad"]
        yas = request.form["yas"]
        cinsiyet = request.form["cinsiyet"]
        kullanici_ad = request.form["kullanici_ad"]
        email = request.form["email"]
        sifre = request.form["sifre"]

        sorgu = "INSERT INTO kullanicilar (id, ad, soyad, yas, cinsiyet, kullanici_ad, email, sifre) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        veri = (str(uuid.uuid4()), isim, soyad, yas, cinsiyet, kullanici_ad, email, sifre)
        db_kayit(sorgu, veri=veri)
        return redirect("/")

@app.route("/giris", methods=["GET", "POST"])
def giris_sayfasi():
    if request.method == "GET":
        return render_template("giris.html")
    elif request.method == "POST":
        isim = request.form["isim"]
        sifre = request.form["sifre"]

        sorgu = "SELECT * FROM kullanicilar WHERE kullanici_ad = ? AND sifre = ?"
        veri = (isim, sifre)
        kayitlar = db_kayit(sorgu, fetch_tipi="all", veri=veri)
        
        if len(kayitlar) == 0:
            return render_template("giris.html", hata="Kullanıcı bilgileri hatalı!")
        else:
            session["ad"] = isim
            session["sifre"] = sifre
            return redirect("/")

@app.route("/cikis") 
def cikis():
    session.pop("ad", None)
    session.pop("sifre", None)
    return redirect("/giris")

if __name__ == "__main__":
    app.run(debug=True)

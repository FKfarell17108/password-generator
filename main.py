from flask import Flask, render_template, request
import random
import string
import hashlib
import os

app = Flask(__name__)

substitusi = {
    'a': '4', 'i': '1', 'e': '3', 'o': '0',
    's': '$', 'g': '9', 'b': '8', 't': '7'
}
simbol_opsional = ['@', '#', '!', '?', '%', '&', '*']

def ubah_karakter(teks):
    return ''.join(substitusi.get(c, c) for c in teks.lower())

def random_kapital(teks):
    return ''.join(c.upper() if random.random() > 0.5 else c for c in teks)

def validasi(pw):
    return (any(c.isupper() for c in pw) and
            any(c.islower() for c in pw) and
            any(c.isdigit() for c in pw) and
            any(c in simbol_opsional for c in pw))

def generate_password(user_input, panjang):
    hasil = ubah_karakter(user_input)
    hasil = random_kapital(hasil)
    hasil = random.choice(simbol_opsional) + hasil + random.choice(simbol_opsional)

    while len(hasil) < panjang:
        hasil += random.choice(string.ascii_letters + string.digits + ''.join(simbol_opsional))

    hasil = list(hasil)
    random.shuffle(hasil)
    pw = ''.join(hasil)

    while not validasi(pw):
        random.shuffle(hasil)
        pw = ''.join(hasil)

    return pw

@app.route("/", methods=["GET", "POST"])
def index():
    password = ''
    hash_pw = ''
    if request.method == "POST":
        user_input = request.form.get("base")
        try:
            panjang = int(request.form.get("length"))
            if not 8 <= panjang <= 16:
                panjang = 12
        except:
            panjang = 12

        password = generate_password(user_input, panjang)
        hash_pw = hashlib.sha256(password.encode()).hexdigest()

    return render_template("index.html", password=password, hash_pw=hash_pw)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
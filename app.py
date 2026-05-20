from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def connect_db():
    conn = sqlite3.connect('studio.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = connect_db()

conn.execute("""
CREATE TABLE IF NOT EXISTS booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    tanggal TEXT,
    jam TEXT,
    studio TEXT,
    metode_bayar TEXT,
    status_bayar TEXT
)
""")

conn.commit()

@app.route('/api/booking', methods=['GET'])
def get_booking():

    conn = connect_db()

    data = conn.execute(
        "SELECT * FROM booking ORDER BY id DESC"
    ).fetchall()

    hasil = []

    for x in data:

        hasil.append({
            "id": x["id"],
            "nama": x["nama"],
            "tanggal": x["tanggal"],
            "jam": x["jam"],
            "studio": x["studio"],
            "metode_bayar": x["metode_bayar"],
            "status_bayar": x["status_bayar"]
        })

    return jsonify(hasil)

@app.route('/api/booking', methods=['POST'])
def add_booking():

    data = request.json

    conn = connect_db()

    cek = conn.execute(
        """
        SELECT * FROM booking
        WHERE tanggal=?
        AND jam=?
        AND studio=?
        """,
        (
            data['tanggal'],
            data['jam'],
            data['studio']
        )
    ).fetchone()

    if cek:

        return jsonify({
            "message":"Jadwal sudah dibooking"
        }), 400

    status = "Belum Bayar"

    if data['metode_bayar'] != "Cash":
        status = "Lunas"

    conn.execute(
        """
        INSERT INTO booking
        (
        nama,
        tanggal,
        jam,
        studio,
        metode_bayar,
        status_bayar
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            data['nama'],
            data['tanggal'],
            data['jam'],
            data['studio'],
            data['metode_bayar'],
            status
        )
    )

    conn.commit()

    return jsonify({
        "message":"Booking berhasil"
    })

@app.route('/api/booking/<int:id>', methods=['DELETE'])
def hapus_booking(id):

    conn = connect_db()

    conn.execute(
        "DELETE FROM booking WHERE id=?",
        (id,)
    )

    conn.commit()

    return jsonify({
        "message":"Booking dibatalkan"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
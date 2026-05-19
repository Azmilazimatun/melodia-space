from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)
CORS(app)

db = MySQLdb.connect(
    host="localhost",
    user="vagrant",
    passwd="vagrant",
    db="db_studio"
)

@app.route('/api/booking', methods=['GET'])
def get_booking():

    cur = db.cursor()

    cur.execute("SELECT * FROM booking ORDER BY id DESC")

    data = cur.fetchall()

    hasil = []

    for x in data:

        hasil.append({

            "id": x[0],
            "nama": x[1],
            "tanggal": str(x[2]),
            "jam": x[3],
            "studio": x[4],
            "metode_bayar": x[5],
            "status_bayar": x[6]

        })

    return jsonify(hasil)

@app.route('/api/booking', methods=['POST'])
def add_booking():

    data = request.json

    cur = db.cursor()

    cur.execute(
        """
        SELECT * FROM booking
        WHERE tanggal=%s
        AND jam=%s
        AND studio=%s
        """,
        (
            data['tanggal'],
            data['jam'],
            data['studio']
        )
    )

    cek = cur.fetchone()

    if cek:

        return jsonify({
            "message":"Jadwal sudah dibooking"
        }), 400

    status = "Belum Bayar"

    if data['metode_bayar'] != "Cash":
        status = "Lunas"

    cur.execute(
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
        VALUES (%s,%s,%s,%s,%s,%s)
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

    db.commit()

    return jsonify({
        "message":"Booking berhasil"
    })

@app.route('/api/booking/<int:id>', methods=['DELETE'])
def hapus_booking(id):

    cur = db.cursor()

    cur.execute(
        "DELETE FROM booking WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({
        "message":"Booking dibatalkan"
    })

app.run(
    host='0.0.0.0',
    port=5000
)

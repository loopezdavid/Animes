from flask import Flask, jsonify, request
import dao_Carrera as dao
import mysql.connector

app = Flask(__name__)

conexion = dao.connect_db("root", "Bootcamp123")
cursor = conexion.cursor(dictionary=True)


@app.route("/ver/carreras", methods=["GET"])
def obtener_carreras():
    carreras = dao.ver_carreras(cursor)
    return jsonify(carreras), 200

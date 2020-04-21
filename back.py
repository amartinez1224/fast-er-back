from flask import Flask
from flask_restful import Api, Resource, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

def getHospitales(connectdb):
    hospitales=[]
    db = connectdb.cursor()
    ids=("id",  "nombre", "lat",  "lng", "disponibilidad")
    db.execute("SELECT %s,  %s, %s, %s, %s  FROM hospitales"%ids)
    result = db.fetchall()
    for h in result:
        hosp=dict(zip(ids,h))
        hosp["lat"]=float(hosp["lat"])
        hosp["lng"]=float(hosp["lng"])
        hospitales.append(hosp)
    return hospitales

def getHospitalesFull(connectdb):
    hospitales=[]
    db = connectdb.cursor()
    ids=("id",  "nombre", "lat",  "lng", "disponibilidad")
    db.execute("SELECT %s,  %s, %s, %s, %s  FROM hospitales"%ids)
    result = db.fetchall()
    for h in result:
        hosp=dict(zip(ids,h))
        hosp["lat"]=float(hosp["lat"])
        hosp["lng"]=float(hosp["lng"])
        especialidades = []
        for esp in getEspecialidadesHospital(connectdb,hosp["id"]):
            especialidad = {}
            especialidad["nombre"] = getEspecialidadesID(connectdb,esp[0])[0][0]
            especialidades.append(especialidad)
        hosp["especialidades"]=especialidades
        hospitales.append(hosp)
    return hospitales

def getEspecialidades(connectdb):
    especialidades=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM especialidades")
    result = db.fetchall()
    for e in result:
        especialidades.append(e)
    return especialidades

def getEspecialidadesID(connectdb,id):
    especialidades=[]
    db = connectdb.cursor()
    db.execute("SELECT nombre FROM especialidades WHERE id = "+str(id))
    result = db.fetchall()
    for e in result:
        especialidades.append(e)
    return especialidades

def getEspecialidadesHospital(connectdb,id):
    esp=[]
    db = connectdb.cursor()
    db.execute("SELECT idEspecialidad FROM especialidadesHosp WHERE idHospital = "+str(id))
    result = db.fetchall()
    for e in result:
        esp.append(e)
    return esp


connectdb = mysql.connector.connect(
  host="XXXXXXXXXX",
  port="3306",
  user="admin",
  passwd="XXXXXXXXXX",
  database="faster"
)

class Hospitales(Resource):
    def get(self):
        global connectdb
        hosp = getHospitalesFull(connectdb)
        return hosp,200

@app.after_request
def add_security_headers(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

api.add_resource(Hospitales,"/hospitales")
app.run(host="0.0.0.0",debug=True)

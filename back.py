from flask import Flask,request
from flask_restful import Api, Resource, reqparse
import mysql.connector
import numpy as np
import json

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

def distancia(lat1,lon1,lat2,lon2):
  R = 6371
  dLat = np.radians(lat2-lat1)
  dLon = np.radians(lon2-lon1);
  a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
  c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
  d = R * c
  return d



connectdb = mysql.connector.connect(
  host="xxxxxxxx",
  port="3306",
  user="admin",
  passwd="xxxxxxxxx",
  database="faster"
)

class Hospitales(Resource):
    def get(self,lat,lang):
        global connectdb
        hosp = getHospitalesFull(connectdb)
        for h in hosp:
            dis = distancia(float(lat),float(lang), h["lat"], h["lng"])
            h["distancia"]=dis
        hosp = sorted(hosp, key=lambda x: x["distancia"])
        return hosp,200

class HospitalesSintomas(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("lat")
        parser.add_argument("lng")
        parser.add_argument("result")
        args = parser.parse_args()
        lat=args["lat"]
        lang=args["lng"]
        j=json.loads(args["result"].replace("\'","\""))["parameters"]
        sintomas = j["sintoma"]
        edad = j["edad"]

        global connectdb
        hosp = getHospitalesFull(connectdb)
        for h in hosp:
            dis = distancia(float(lat),float(lang), h["lat"], h["lng"])
            h["distancia"]=dis
        hosp = sorted(hosp, key=lambda x: x["distancia"])

        return (lat,lang,sintomas,edad),201

@app.after_request
def add_security_headers(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

api.add_resource(Hospitales,"/hospitales/<lat>/<lang>")
api.add_resource(HospitalesSintomas,"/hospitales/sintomas")
app.run(host="0.0.0.0",debug=True)

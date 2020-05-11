from flask import Flask,request
from flask_restful import Api, Resource, reqparse
import mysql.connector
import numpy as np
import json
from difflib import SequenceMatcher



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

def getEspecialidadesSintomas(connectdb, id):
    hospEsp=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM especialidadesSin WHERE idSintoma = "+str(id))
    result = db.fetchall()
    for he in result:
        hospEsp.append(he)
    return hospEsp

def getSintomas(connectdb):
    especialidades=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM sintomas")
    result = db.fetchall()
    for e in result:
        especialidades.append(e)
    return especialidades

def distancia(lat1,lon1,lat2,lon2):
    R = 6371
    dLat = np.radians(lat2-lat1)
    dLon = np.radians(lon2-lon1);
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

connectdb = mysql.connector.connect(
  host="xxxxxxxxx",
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
        hosp = sorted(hosp, key=lambda x: x["distancia"])[:8]

        palabras = []
        [palabras.extend(s.lower().split(" ")) for s in sintomas]
        sintomas = getSintomas(connectdb)

        idSintomas=[]
        for p in palabras:
            for s in sintomas:
                #print(p,s[1],similar(p,s[1]))
                if similar(p,s[1])>0.8:
                    idSintomas.append(s[0])
                    sintomas.remove(s)

        if len(idSintomas)>0:
            especialidades=[]
            for id in idSintomas:
                especialidades.extend([esp[0] for esp in getEspecialidadesSintomas(connectdb,id)])

            especialidad=max(set(especialidades), key = especialidades.count)


            second=[]
            for h in hosp:
                esp = getEspecialidadesHospital(connectdb,h["id"])

                if especialidad not in h:
                    second.append(h)
                    hosp.remove(h)
            hosp.extend(second)


        return hosp,201

app = Flask(__name__)
api = Api(app)

@app.after_request
def add_security_headers(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp

api.add_resource(Hospitales,"/hospitales/<lat>/<lang>")
api.add_resource(HospitalesSintomas,"/hospitales/sintomas")
app.run(host="0.0.0.0",debug=True)

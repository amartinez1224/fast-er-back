import mysql.connector

def createTableHospitales(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE hospitales (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), lat DECIMAL(10,8), lng DECIMAL(10,8), disponibilidad INTEGER)")
    connectdb.commit()

def createTableEspecialidades(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE especialidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    connectdb.commit()

def createTableEspecialidadesHospitales(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE especialidadesHosp (idHospital INT, FOREIGN KEY (idHospital) REFERENCES hospitales(id) ON DELETE CASCADE, idEspecialidad INT, FOREIGN KEY (idEspecialidad) REFERENCES especialidades(id) ON DELETE CASCADE)")
    connectdb.commit()

def insertHospitales(connectdb):
    sql = "INSERT INTO hospitales (nombre, lat, lng, disponibilidad) VALUES (%s, %s, %s, %s)"
    val = [
      ("Fundacion Cardio Infantil","4.741398","-74.034290","10"),
      ("Hospital Simon Bolivar","4.742458","-74.022652","10")
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertEspecialidades(connectdb):
    sql = "INSERT INTO especialidades (nombre) VALUES (%s)"
    val = [
      ("Neurologia",),
      ("Cardiologia",)
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertEspecialidadesHospitales(connectdb):
    sql = "INSERT INTO especialidadesHosp  (idHospital, idEspecialidad) VALUES (%s, %s)"
    val = [
      ("1","1"),
      ("2","1"),
      ("2","2")
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def dropHospitales(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS hospitales"
    db.execute(sql)
    connectdb.commit()

def dropEspecialidades(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS especialidades"
    db.execute(sql)
    connectdb.commit()

def dropEspecialidadesHospitales(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS especialidadesHosp"
    db.execute(sql)
    connectdb.commit()

def getHospitales(connectdb):
    hospitales=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM hospitales")
    result = db.fetchall()
    for h in result:
        hospitales.append(h)
    return hospitales

def getEspecialidades(connectdb):
    especialidades=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM especialidades")
    result = db.fetchall()
    for e in result:
        especialidades.append(e)
    return especialidades

def getEspecialidadesHospitales(connectdb):
    hospEsp=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM especialidadesHosp")
    result = db.fetchall()
    for he in result:
        hospEsp.append(he)
    return hospEsp


connectdb = mysql.connector.connect(
  host="XXXXXXXXXX",
  port="3306",
  user="admin",
  passwd="XXXXXXXXXX",
  database="faster"
)

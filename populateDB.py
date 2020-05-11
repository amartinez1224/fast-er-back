import mysql.connector

def createTableHospitales(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE hospitales (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), lat DECIMAL(10,8), lng DECIMAL(10,8), disponibilidad INTEGER)")
    connectdb.commit()

def createTableEspecialidades(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE especialidades (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    connectdb.commit()

def createTableSintomas(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE sintomas (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))")
    connectdb.commit()

def createTableEspecialidadesHospitales(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE especialidadesHosp (idHospital INT, FOREIGN KEY (idHospital) REFERENCES hospitales(id) ON DELETE CASCADE, idEspecialidad INT, FOREIGN KEY (idEspecialidad) REFERENCES especialidades(id) ON DELETE CASCADE)")
    connectdb.commit()

def createTableEspecialidadesSintomas(connectdb):
    db = connectdb.cursor()
    db.execute("CREATE TABLE especialidadesSin (idEspecialidad INT, FOREIGN KEY (idEspecialidad) REFERENCES especialidades(id) ON DELETE CASCADE, idSintoma INT, FOREIGN KEY (idSintoma) REFERENCES sintomas(id) ON DELETE CASCADE)")
    connectdb.commit()

def insertHospitales(connectdb):
    sql = "INSERT INTO hospitales (nombre, lat, lng, disponibilidad) VALUES (%s, %s, %s, %s)"
    val = [
      ("Fundacion Cardio Infantil","4.741398","-74.034290","10"),
      ("Hospital Simon Bolivar","4.742458","-74.022652","10"),
      ("Clinica Reina Sofia","4.706891","-74.051986","10"),
      ("Hospital de la Policia","4.647038","-74.097935","10"),
      ("Clinica del Country","4.669316","-74.057110","10"),
      ("Clinica Shaio","4.698287","-74.073219","10"),
      ("Hospital de Kennedy","4.616447","-74.153303","10"),
      ("Hospital El Tintal","4.651496","-74.148940","10"),
      ("Hospital San Juan de Dios","4.588883","-74.086509","10"),
      ("Hospital San Carlos","4.570616","-74.106565","10"),
      ("Clinica Colombia","4.648450","-74.106731","10")
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertEspecialidadesHospitales(connectdb):
    sql = "INSERT INTO especialidadesHosp  (idHospital, idEspecialidad) VALUES (%s, %s)"
    val = [
      ("1","1"),("1","5"),
      ("2","1"),("2","2"),
      ("3","1"),
      ("4","1"),("4","4"),
      ("5","1"),
      ("6","1"),
      ("7","1"),
      ("8","1"),("8","4"),
      ("9","1"),
      ("10","1"),
      ("11","1"),("10","3")
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertEspecialidades(connectdb):
    sql = "INSERT INTO especialidades (nombre) VALUES (%s)"
    val = [
      ("General",),
      ("Neurologia",),
      ("Respiratorio",),
      ("Trauma",),
      ("Cardiologia",)
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertSintomas(connectdb):
    sql = "INSERT INTO sintomas (nombre) VALUES (%s)"
    val = [
      ("cabeza",),
      ("estomago",),
      ("brazo",),
      ("pierna",),
      ("pecho",),
      ("herida",),
      ("sangre",),
      ("respirar",),
      ("golpe",),
      ("delirar",),
      ("dolor",)
    ]
    db = connectdb.cursor()
    db.executemany(sql, val)
    connectdb.commit()

def insertEspecialidadesSintomas(connectdb):
    sql = "INSERT INTO especialidadesSin  (idEspecialidad, idSintoma) VALUES (%s, %s)"
    val = [
      ("1","1"),("1","2"),("1","9"),("1","11"),
      ("2","1"),("2","10"),("2","1"),
      ("3","8"),
      ("4","1"),("4","3"),("4","4"),("4","6"),("4","7"),("4","9"),
      ("5","5"),("5","11"),("5","3")
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

def dropSintomas(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS sintomas"
    db.execute(sql)
    connectdb.commit()

def dropEspecialidadesHospitales(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS especialidadesHosp"
    db.execute(sql)
    connectdb.commit()

def dropEspecialidadesSintomas(connectdb):
    db = connectdb.cursor()
    sql = "DROP TABLE IF EXISTS especialidadesSin"
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

def getSintomas(connectdb):
    especialidades=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM sintomas")
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

def getEspecialidadesSintomas(connectdb):
    hospEsp=[]
    db = connectdb.cursor()
    db.execute("SELECT * FROM especialidadesSin")
    result = db.fetchall()
    for he in result:
        hospEsp.append(he)
    return hospEsp


connectdb = mysql.connector.connect(
  host="xxxxxxxxx",
  port="3306",
  user="admin",
  passwd="xxxxxxxxx",
  database="faster"
)

if __name__ == "__main__":

    dropEspecialidadesSintomas(connectdb)
    dropEspecialidadesHospitales(connectdb)
    dropEspecialidades(connectdb)
    dropSintomas(connectdb)
    dropHospitales(connectdb)

    createTableSintomas(connectdb)
    createTableHospitales(connectdb)
    createTableEspecialidades(connectdb)
    createTableEspecialidadesHospitales(connectdb)
    createTableEspecialidadesSintomas(connectdb)

    insertSintomas(connectdb)
    insertHospitales(connectdb)
    insertEspecialidades(connectdb)
    insertEspecialidadesHospitales(connectdb)
    insertEspecialidadesSintomas(connectdb)

    print("\n----------- Hospitales -----------")
    print(getHospitales(connectdb))
    print("\n--------- Especialidades ---------")
    print(getEspecialidades(connectdb))
    print("\n------------ Sintomas ------------")
    print(getSintomas(connectdb))
    print("\n----- Hospital-Especialidad ------")
    print(getEspecialidadesHospitales(connectdb))
    print("\n------ Especialidad-Sintoma ------")
    print(getEspecialidadesSintomas(connectdb))

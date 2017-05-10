import requests
import json
import pymysql
import sys


CONF_DB = {"HOST" : "localhost",
           "USER" : "cp",
           "PASS" : "cp",
           "DB" : "cp",
           "CHARSET" : "utf8mb4",
           "CURSORCLASS" : pymysql.cursors.DictCursor}
OFFSET = 30
EPICENTRO = (-34.5639222,-58.45990419999998)
HEADERS = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96",
           "Referer": "https://www.preciosclaros.gob.ar/",
           "Origin": "https://www.preciosclaros.gob.ar/",
           "User-Agent": None}




def conectDB():
    return pymysql.connect(host = CONF_DB["HOST"],
                           user = CONF_DB["USER"],
                           password = CONF_DB["PASS"],
                           db = CONF_DB["DB"],
                           charset = CONF_DB["CHARSET"],
                           cursorclass = CONF_DB["CURSORCLASS"])

def createSucursalesTable():
    db = conectDB()
    db.cursor().execute("CREATE TABLE Sucursales (sucursalNombre varchar(255),provincia varchar(255),localidad varchar(255),lng varchar(255),lat varchar(255),sucursalTipo varchar(255),banderaDescripcion varchar(255),comercioId int,distanciaDescripcion varchar(255),comercioRazonSocial varchar(255),sucursalId varchar(255),distanciaNumero double,banderaId int,id varchar(255),direccion varchar(255),PRIMARY KEY (id));")
    db.close()


#trae las sucursales de un nivel especifico
def getSucursalesNivel(epicentro=(0.0,0.0),nivel=3):
    if epicentro == (0.0,0.0):
        epicentro = EPICENTRO
    url = "https://d3e6htiiul5ek9.cloudfront.net/dev/sucursales?limit="+str(OFFSET)+"&lat="+str(epicentro[0])+"&lng="+str(epicentro[1])+"&offset="+str(OFFSET*nivel)
    r = requests.get(url,headers=HEADERS)
    return r.json()["sucursales"]


def setSucursalesInTab(sucursales):
    db = conectDB()
    for s in sucursales:
        q = "INSERT INTO Sucursales(sucursalNombre,provincia,localidad,lng,lat,sucursalTipo,banderaDescripcion,comercioId,distanciaDescripcion,comercioRazonSocial,sucursalId,distanciaNumero,banderaId,id,direccion) VALUES('"+str(s["sucursalNombre"])+"','"+str(s["provincia"])+"','"+str(s["localidad"])+"','"+str(s["lng"])+"','"+str(s["lat"])+"','"+str(s["sucursalTipo"])+"','"+str(s["banderaDescripcion"])+"','"+str(s["comercioId"])+"','"+str(s["distanciaDescripcion"])+"','"+str(s["comercioRazonSocial"])+"','"+str(s["sucursalId"])+"','"+str(s["distanciaNumero"])+"','"+str(s["banderaId"])+"','"+str(s["id"])+"','"+str(s["direccion"])+"');"
        try:
            db.cursor().execute(q)
            db.commit()
        #con esto no putea cuando hay un valor duplicado
        except pymysql.err.IntegrityError:
            pass
        except:
            db.roolback()
    db.close()


#siempre cuenta desde 0
def getIdSucursales(cantidad=0,pagina=0):
    db = conectDB()
    q = "SELECT id from Sucursales ORDER BY distanciaNumero LIMIT "+str(cantidad*pagina)+","+str(cantidad)+";"
    cursor = db.cursor()
    try:
        cursor.execute(q)
        result = cursor.fetchall()
    finally:
        db.close()
    return result




#s = getSucursalesNivel(nivel=0)
#print(s)
#print(len(s))
#createSucursalesTable()
#setSucursalesInTab(s)
#print()
#print(getIdSucursales(50,0))
#print(len(getIdSucursales(50,0)))

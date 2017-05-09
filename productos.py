import requests
import json
import pymysql



CONF_DB = {"HOST" : "localhost",
           "USER" : "cp",
           "PASS" : "cp",
           "DB" : "cp",
           "CHARSET" : "utf8mb4",
           "CURSORCLASS" : pymysql.cursors.DictCursor}
CANTIDAD = 100
HEADERS = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}

_PRODUCTO="string=leche&" #TODO ESTO ES UNA VARIABLE PARA HACER PRUEBAS, BORRAR EN LA VERSION FINAL


def conectDB():
    return pymysql.connect(host = CONF_DB["HOST"],
                           user = CONF_DB["USER"],
                           password = CONF_DB["PASS"],
                           db = CONF_DB["DB"],
                           charset = CONF_DB["CHARSET"],
                           cursorclass = CONF_DB["CURSORCLASS"])





#obtiene la cantidad de productos indicada, para una pagina indicada, para la lista de sucursales que se le pasa
#la lista de sucursales como maximo puede tener 50 sucursales
#puede traer hasta 100 productos por consulta
#sucursales es una lista que en cada campo tiene el codigo de sucursal (campo id)
def getProductosPagina(sucursales,cantidad=CANTIDAD,pagina=0):
    suc = ""
    for x in sucursales:
        suc += x+","
    suc = suc[-1]
    url= "https://d3e6htiiul5ek9.cloudfront.net/prod/productos?"+_PRODUCTO+"array_sucursales="+suc+"&offset="+str(cantidad*pagina)+"&limit="+str(cantidad)
    r = requests.get(url,headers=HEADERS)
    return r.json()["productos"]



def createProductosTable():
    db = conectDB()
    q = "CREATE TABLE Productos(marca varchar(255),id varchar(255),nombre varchar(255),presentacion varchar(255),PRIMARY KEY (id))"
    db.cursor().execute(q)    
    db.close()


def setProductosInTab(productos):
    db = conectDB()
    for p in productos:
        q = "INSET INTO Productos(marca,id,nombre,presentacion)VALUES('"+str(p["marca"])+"','"+str(p["id"])+"','"+str(p["nombre"])+"','"+str(p["presentacion"])+"')"
        try:
            db.cursor().execute(q)
            db.commit()
        #con esto no putea cuando hay un valor duplicado
        except pymysql.err.IntegrityError:
            pass
        except:
            db.roolback()
    db.close()




def getIdProductos(cantidad=CANTIDAD,pagina=0):
    db = conectDB()
    q = "SELECT id from Productos LIMIT "+str(cantidad*pagina)+","+str(cantidad)+";"
    cursor = db.cursor()
    try:
        cursor.execute(q)
        result = cursor.fetchall()
    finally:
        db.close()
    return result
















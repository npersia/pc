import requests
import json
import pymysql





#ejemplo de conexion y uso de mysql http://www.w3big.com/es/python3/python3-mysql.html
#docker run --rm --name cp_bd -p 3306:3306 -e MYSQL_ROOT_PASSWORD=npersia -e MYSQL_DATABASE=cp -e MYSQL_USER=cp -e MYSQL_PASSWORD=cp mysql
#db=pymysql.connect("localhost","cp","cp","cp" )
#cursor = db.cursor()
#cursor.execute("SELECT VERSION()")
#data = cursor.fetchone()
#print ("Database version : %s " % data)
#db.close()





def setDB():
    HOST = "localhost"
    USER = "cp"
    PASS = "cp"
    DB = "cp"
    return pymysql.connect("localhost","cp","cp","cp" )


def setTabComercios(cursor):
    cursor.execute("CREATE TABLE Comercios (sucursalNombre varchar(255),provincia varchar(255),localidad varchar(255),lng varchar(255),lat varchar(255),sucursalTipo varchar(255),banderaDescripcion varchar(255),comercioId int,distanciaDescripcion varchar(255),comercioRazonSocial varchar(255),sucursalId varchar(255),distanciaNumero double,banderaId int,id varchar(255),direccion varchar(255),PRIMARY KEY (id));")

def setComerciosInTab(db,cursor,comercios):
    for c in comercios:
        q = "INSERT INTO Comercios(sucursalNombre,provincia,localidad,lng,lat,sucursalTipo,banderaDescripcion,comercioId,distanciaDescripcion,comercioRazonSocial,sucursalId,distanciaNumero,banderaId,id,direccion) VALUES('"+str(c["sucursalNombre"])+"','"+str(c["provincia"])+"','"+str(c["localidad"])+"','"+str(c["lng"])+"','"+str(c["lat"])+"','"+str(c["sucursalTipo"])+"','"+str(c["banderaDescripcion"])+"','"+str(c["comercioId"])+"','"+str(c["distanciaDescripcion"])+"','"+str(c["comercioRazonSocial"])+"','"+str(c["sucursalId"])+"','"+str(c["distanciaNumero"])+"','"+str(c["banderaId"])+"','"+str(c["id"])+"','"+str(c["direccion"])+"');"
        try:
            cursor.execute(q)
            db.commit()
        #con esto no putea cuando hay un valor duplicado
        except pymysql.err.IntegrityError:
            pass
        except:
            db.roolback()

    cursor.execute("select * from Comercios;")
    for r in cursor.fetchall():
        print(r)





#funcionalidad para meter comercios en la base de datos
c = getComercios(nivel=3)
#print(c)
db = setDB()
#setTabComercios(db.cursor())
setComerciosInTab(db,db.cursor(),c)
db.close()


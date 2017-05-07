import requests
import json
import pymysql


# geti es un ejemplo
def geti():
    headers = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}
    url="https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=leche&array_sucursales=12-1-47,11-1-1102,10-2-182,10-3-671,10-3-325,10-3-320,10-3-361,10-3-683,10-3-311,9-2-38,10-2-120,3-1-599,10-3-674,10-3-617,10-3-739,10-3-632,10-3-351,9-2-977,12-1-44,9-2-12,12-1-22,10-3-613,10-3-391,10-3-568,10-3-721,10-3-551,9-2-14,9-2-54,10-3-335,10-3-343&offset=0&limit=50&sort=-cant_sucursales_disponible"
    r = requests.get(url,headers=headers)
    
    return r.json()

#print(geti()['total'])



#sucursales
#https://d3e6htiiul5ek9.cloudfront.net/dev/sucursales?limit=30&offset=0

#sucursales con cercania
#https://d3e6htiiul5ek9.cloudfront.net/dev/sucursales?limit=30&offset=0&lat=-34.5639222&lng=-58.45990419999998



#devuelve los comercios
def getComercios(epicentro="",nivel=3):
    offset = 30
    epic = "lat=-34.5639222&lng=-58.45990419999998"#epicentro
    headers = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}
    suc = []
    for x in range(nivel):
        url = "https://d3e6htiiul5ek9.cloudfront.net/dev/sucursales?limit="+str(offset)+"&"+epic+"&offset="+str(offset*x)
        r = requests.get(url,headers=headers)
        suc.extend(r.json()["sucursales"])
    return suc

def getIdComercios(lComercios):
    idCom = []
    for c in lComercios:
        idCom.append(c["id"])
    return idCom


#devuelve los productos para una lista de Comercios, maximo para 50 comercios
def getProductos(comercios):
    com = str(comercios).replace("'","").replace("[","").replace("]","")
    offset = 100
    headers = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}
    prod = []
    
    x = 0
    PAGINAS = 1
    while PAGINAS > x:
        url= "https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=leche&array_sucursales="+com+"&offset="+str(offset*x)+"&limit="+str(offset)
        r = requests.get(url,headers=headers)
        #print(r.json()["productos"])
        prod.extend(r.json()["productos"])
        TOTAL = int(r.json()["total"])
        if TOTAL%offset > 0:
            PAGINAS = (TOTAL//offset) + 1
        else:
            PAGINAS = (TOTAL//offset)
        x += 1
        print(TOTAL)
    return prod
    

#Cuando sean muchos comercios esta funcion sabe partirlos
def getProd(comercios):
    MAX_COMERCIOS = 50
    PRODUCTOS = []
    if len(comercios) <= MAX_COMERCIOS:
        return getProductos(comercios)
    else:
        if len(comercios)%MAX_COMERCIOS > 0:
            HASTA = (len(comercios)/MAX_COMERCIOS)+1
        else:
            HASTA = len(comercios)/MAX_COMERCIOS
        for x in range(0,int(HASTA)):
            PRODUCTOS.extend(getProductos(comercios[x*MAX_COMERCIOS:(x+1)*MAX_COMERCIOS]))
        return PRODUCTOS



#c = getComercios(nivel=3)
#print(c)
#idC = getIdComercios(c)
#print(idC)
#print(getProductos(idC))
#print(len(idC))
#prods=getProd(idC)
#print(prods)
#print(len(prods))















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

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
def getProductos(sucursales,cantidad=CANTIDAD,pagina=0):
    suc = ""
    for x in sucursales:
        suc += x+","
    suc = suc[-1]
    url= "https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=leche&array_sucursales="+suc+"&offset="+str(cantidad*pagina)+"&limit="+str(cantidad)
    r = requests.get(url,headers=HEADERS)
    return r.json()["productos"]


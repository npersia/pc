import requests
import json
import pymysql



CONF_DB = {"HOST" : "localhost",
           "USER" : "cp",
           "PASS" : "cp",
           "DB" : "cp",
           "CHARSET" : "utf8mb4",
           "CURSORCLASS" : pymysql.cursors.DictCursor}
OFFSET = 30
HEADERS = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}




def conectDB():
    return pymysql.connect(host = CONF_DB["HOST"],
                           user = CONF_DB["USER"],
                           password = CONF_DB["PASS"],
                           db = CONF_DB["DB"],
                           charset = CONF_DB["CHARSET"],
                           cursorclass = CONF_DB["CURSORCLASS"])





#
def getProductos(comercios):
    com = str(comercios)replace("'","").replace("[","").replace("]","")
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


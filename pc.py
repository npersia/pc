import requests
import json

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
    


#devuelve los productos para una lista de Comercios, maximo para 50 comercios
#def getProductos(comercios):
#    com = str(comercios).replace("'","").replace("[","").replace("]","")
#    offset = 100
#    headers = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}
#    prod = []
#    for x in range(99999):
#        url= "https://d3e6htiiul5ek9.cloudfront.net/prod/productos?array_sucursales="+com+"&offset="+str(offset*x)+"&limit="+str(offset)
#        r = requests.get(url,headers=headers)
#        print(r.json()["productos"])
#        prod.extend(r.json()["productos"])
#        if (offset*x) > int(r.json()["total"]):
#            break
#    return prod








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



c = getComercios(nivel=3)
print(c)
idC = getIdComercios(c)
print(idC)
#print(getProductos(idC))
#print(len(idC))
#prods=getProd(idC)
#print(prods)
#print(len(prods))


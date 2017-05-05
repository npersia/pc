import requests
import json

#r = requests.get("http://localhost:8001/weathercondition?lat=-34.6421149&lon=-58.4612144")

def geti():
    headers = {"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/","User-Agent": None}
    url="https://d3e6htiiul5ek9.cloudfront.net/prod/productos?string=leche&array_sucursales=12-1-47,11-1-1102,10-2-182,10-3-671,10-3-325,10-3-320,10-3-361,10-3-683,10-3-311,9-2-38,10-2-120,3-1-599,10-3-674,10-3-617,10-3-739,10-3-632,10-3-351,9-2-977,12-1-44,9-2-12,12-1-22,10-3-613,10-3-391,10-3-568,10-3-721,10-3-551,9-2-14,9-2-54,10-3-335,10-3-343&offset=0&limit=50&sort=-cant_sucursales_disponible"
    #r = requests.get(url,headers={"x-api-key": "zIgFou7Gta7g87VFGL9dZ4BEEs19gNYS1SOQZt96","Referer": "https://www.preciosclaros.gob.ar/","Origin": "https://www.preciosclaros.gob.ar/"})
    r = requests.get(url,headers=headers)
    
    return r.json()




print(geti()['total'])

#!/usr/bin/python3

import sucursales
import productos


s = sucursales.getSucursalesNivel(nivel=0)
print(s)
print(len(s))
sucursales.createSucursalesTable()
sucursales.setSucursalesInTab(s)
print()
q=sucursales.getIdSucursales(50,0)
print(q)


a=[]
for x in q:
    a.extend(x.values())

print(a)


productos.createProductosTable()
p = productos.getProductosPagina(a,100,0)

print()
print(p)

productos.setProductosInTab(p)

print(productos.getIdProductos())

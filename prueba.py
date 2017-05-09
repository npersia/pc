import sucursales
import productos


s = sucursales.getSucursalesNivel(nivel=0)
print(s)
print(len(s))

sucursales.createSucursalesTable()
sucursales.setSucursalesInTab(s)
print()
print(sucursales.getIdSucursales(50,0))

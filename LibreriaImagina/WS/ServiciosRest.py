# import request 
import requests

uri = "http://localhost:50929/api/Servicios"

# cliente
cliente = requests.get(uri)

if cliente.status_code== 200:
  servicios = cliente.json()
  
  for x in servicios:
    print(f"{x['Rut']} {x['Nombre']} {x['TipoServicio']} {x['Fecha']}")
else:
  print("Error con la API")
  
  
# Buscar por rut
rut = input("Ingrese rut: ")
cliente = requests.get(f"{uri}?rut={rut}")

if cliente.status_code== 200:
  serv = cliente.json()
  
  if serv!=None:
    print(f"{serv['Rut']} {serv['Nombre']} {serv['TipoServicio']} {serv['Fecha']}")
  else:
    print("No existe el rut")

  
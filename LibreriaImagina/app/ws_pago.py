import requests
from .views import pagoTarjeta
from zeep import Client

# craecion cliente
cliente = Client("http://localhost:8080/WsPago_de_una(G)/WsPago_de_una?WSDL")


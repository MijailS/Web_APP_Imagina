from django.urls import path
from .views import catalogoInsumos , despacho, registroCliente, home, catalogoproducto, pagar, pagoCompletado, pagoTarjeta, quienesSomos, seguimiento, agendaLista, agendaMenu, reservas, loginCliente, agregar_producto, eliminar_producto, restar_producto, vaciar_carrito, carrito, verdespacho

urlpatterns = [
    path('', home, name="home"),
    path('catalogoproducto/', catalogoproducto, name="catalogoproducto"),
    path('catalogoinsumos/', catalogoInsumos, name="catalogoinsumos"),
    path('pagar/', pagar, name="pagar"),
    path('pagoCompletado/', pagoCompletado, name="pagoCompletado"),
    path('pagoTarjeta/', pagoTarjeta, name="pagoTarjeta"),
    path('quienesSomos/', quienesSomos, name="quienesSomos"),
    path('registroCliente/', registroCliente, name='registroCliente'),
    path('seguimiento/', seguimiento, name="seguimiento"),
    path('agendaLista/', agendaLista, name="agendaLista"),
    path('agendaMenu/', agendaMenu, name="agendaMenu"),
    path('reservas/', reservas, name="reservas"),
    path('carrito/', carrito, name='carrito'),
    path('carrito/agregar/<int:libro_id>/', agregar_producto, name='agregar_producto'),
    path('carrito/restar/<int:libro_id>/', restar_producto, name='restar_producto'),
    path('carrito/eliminar/<int:libro_id>/', eliminar_producto, name='eliminar_producto'),
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),
    path('verdespacho/', verdespacho, name='verdespacho'),
    path('despacho/', despacho, name='despacho'),
    path('loginCliente/',loginCliente, name ='loginCliente') #no debe ir al proceso sino a template 

]

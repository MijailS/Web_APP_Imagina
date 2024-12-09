from .carrito import Carrito

def carrito_total(request):
    carrito = Carrito(request)
    total = carrito.get_carrito_total()
    return {'total_carrito': total}
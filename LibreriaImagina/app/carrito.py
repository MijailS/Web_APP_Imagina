from .models import Libro

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito', {})
        self.carrito = carrito

    def agregar_producto(self, libro_id):
        existe = False
        id = str(libro_id)

        for key, cantidad in self.carrito.items():
            if key == id:
                existe = True
                break

        if not existe:
            self.carrito[id] = 1
        else:
            self.carrito[id] += 1

        self.guardar_carrito()
    
    def restar_producto(self, libro_id):
        id = str(libro_id)
        cantidad = self.carrito.get(id, 0)
        if cantidad > 1:
            self.carrito[id] = cantidad - 1
        else:
            del self.carrito[id]
        self.guardar_carrito()
        
    
    def eliminar_producto(self, libro_id):
        id = str(libro_id)
        if id in self.carrito:
            del self.carrito[id]
        self.guardar_carrito()
    
    def vaciar_carrito(self):
        self.carrito = {}
        self.guardar_carrito()
    
    def guardar_carrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True
        
    """ def obtener_total(self):
        total = 0
        for libro_id, libro_info in self.carrito.items():
            libro = Libro.objects.get(pk=libro_id)
            total += libro.VALOR * libro_info  # Cambio: obtén directamente la cantidad
        return total """
    
    # def get_carrito_total(self):
        
    #     carrito = self.carrito
    #     libros = []
    #     for libro_id,cantidad in carrito.items():
    #         libro = Libro.objects.get(pk=libro_id)
    #         subtotal = libro.VALOR * cantidad
    #         print("libro")
    #         libros.append({
    #         'img': libro.IMG,  # Supongamos que hay un campo en el modelo "Libro" llamado "imagen_url"
    #         'titulo': libro.TITULO,
    #         'libro_id': libro.ID_LIBRO,
    #         'cantidad': cantidad,
    #         'subtotal': subtotal,
            
    #     })
    #     return libros
    
    def get_carrito_total(self):
        total = 0
        carrito = self.carrito
        for libro_id, cantidad in carrito.items():
            libro = Libro.objects.get(pk=libro_id)
            total += libro.VALOR * cantidad
            # libros={
            #     'img': libro.IMG,
            #     'titulo': libro.TITULO,
            #     'libro_id': libro.ID_LIBRO,
            # }
            # libro.append(libros)
        return total
        
from django.db import models
from django.contrib.auth.models import AbstractUser

class Libro(models.Model):
  ID_LIBRO = models.IntegerField(primary_key=True)
  ISBN = models.IntegerField()
  TITULO = models.CharField(max_length=200)
  VALOR = models.IntegerField()
  PAGINAS = models.IntegerField()
  STOCK = models.IntegerField()
  IMG = models.CharField(max_length=500)
  AUTOR = models.CharField(max_length=70)
  ANIO_EDICION = models.IntegerField()
  RESENIA = models.CharField(max_length=500)
  
  def __str__(self):
    return self.ID_LIBRO
  
  class Meta:
        db_table = 'app_libro'  

class Producto(models.Model):
    nombre = models.CharField(max_length=64)
    categoria = models.CharField(max_length=32)
    precio = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} -> {self.precio}'



opciones_servicio = [
  [0, "a"],
  [1, "b"],
  [2, "c"],
  [4, "d"]
]

class Contacto(models.Model):
  nombre = models.CharField(max_length=50)
  correo = models.EmailField()
  tipo_consulta = models.IntegerField(choices=opciones_servicio)
  mensaje = models.TextField()
  avisos = models.BooleanField()

  def __str__(self):
    return self.nombre
  
class Tecnico(models.Model):
    id_tecnico = models.AutoField(primary_key=True, db_column='ID_TECNICO')
    nombre_completo = models.CharField(max_length=50, db_column='NOMBRE_COMPLETO')

    def __str__(self):
        return self.nombre_completo

class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True, db_column='ID_VISITA')
    fecha = models.DateField(db_column='FECHA')
    hora = models.TimeField(db_column='HORA')
    descripcion = models.CharField(max_length=500, db_column='DESCRIPCION')
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, db_column='TECNICO_ID_TECNICO')

    def __str__(self):
        return f"Visita #{self.id_visita}"
    

class PagoTarjeta(models.Model):
  id_pago = models.AutoField(primary_key=True)
  numero_tarjeta = models.IntegerField()
  cvv = models.IntegerField()
  fecha_vencimiento = models.CharField(max_length=5)

  def __str__(self):
    return self.id_pago


class Insumo(models.Model):
   ID_INSUMO = models.IntegerField(primary_key=True)
   NOMBRE = models.CharField(max_length=200)
   VALOR = models.IntegerField()
   STOCK = models.IntegerField()
   IMG = models.CharField(max_length=500)

   def __str__(self):
      return self.ID_INSUMO

class Venta(models.Model):
   ID_VENTA = models.IntegerField(primary_key=True)
   
   
   def __str__(self):
      return self.ID_INSUMO
from django.db import connection
from django.shortcuts import render, redirect, redirect

from .carrito import Carrito
from .models import Libro, Producto
import cx_Oracle
from .forms import ClienteForm, ContactoForm, CustomUserCreationForm, PagoForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .carrito import Carrito
from .utils import obtener_nombres_comunas

import requests
from django.http import HttpResponse
from zeep import Client
import datetime

# Create your views here.


def base(request):
  return render(request, 'app/base.html')

def home(request):
  return render(request, 'app/home.html')

def catalogoproducto(request):
    # Realizar la conexión a la base de datos Oracle
    conn = cx_Oracle.connect('BASE_DATOS_CSHARP', '1234', 'localhost:1521/orcl')
    cursor = conn.cursor()

    # Declarar el cursor de salida para los resultados del procedimiento almacenado
    libros = cursor.var(cx_Oracle.CURSOR)

    # Ejecutar el procedimiento almacenado
    cursor.callproc('SP_LISTAR_LIBROS', [libros])

    # Obtener los resultados del cursor de salida
    resultados = libros.getvalue().fetchall()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Pasar los resultados a la plantilla y renderizar la vista
    return render(request, 'app/catalogoproducto.html', {'libros': resultados})

def verdespacho(request):
    if request.method == 'POST':
        id_despacho = request.POST.get('id_despacho')
        # Realizar la conexión a la base de datos Oracle
        conn = cx_Oracle.connect('BASE_DATOS_CSHARP', '1234', 'localhost:1521/orcl')
        cursor = conn.cursor()

        # Declarar el cursor de salida para los resultados del procedimiento almacenado
        despachos = cursor.var(cx_Oracle.CURSOR)

        # Ejecutar el procedimiento almacenado para buscar el despacho por ID
        cursor.callproc('SP_BUSCAR_DESPACHO', [id_despacho, despachos])

        # Obtener el resultado del cursor de salida
        despacho = despachos.getvalue().fetchone()

        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

        # Mapear el valor numérico de estado_id_estado a su descripción correspondiente
        estado_id_estado_map = {
            1: 'SOLICITUD RECIBIDA',
            2: 'PEDIDO CONFIRMADO',
            3: 'PEDIDO EN PROCESO DE DESPACHO',
            4: 'PEDIDO ENTREGADO',
            5: 'PEDIDO CANCELADO'
        }

        # Obtener el valor de estado_id_estado del despacho y su descripción correspondiente
        estado_id_estado = despacho[5]
        estado_descripcion = estado_id_estado_map.get(estado_id_estado)

        # Pasar el despacho y su descripción de estado a la plantilla y renderizar la vista
        return render(request, 'app/verdespacho.html', {'despacho': despacho, 'estado_descripcion': estado_descripcion})

    return render(request, 'app/verdespacho.html')

def solicitud_visita(request):
  return render(request, 'app/solicitud_visita.html')

def carrito(request):
    id_libro = request.session.get('libro_id')
    print("Funciono!!",id_libro)
    carrito = Carrito(request)
    total = carrito.get_carrito_total()
    try:
      conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
      cursor = conn.cursor()
      # v_salida = cursor.var(cx_Oracle.STRING)
      cursor.callproc('SP_BUSCAR_LIBRO', [id_libro])
      # resultado = v_salida.getvalue()
      cursor.close()
      conn.close()
      # if resultado is not None:

      #   print("Funciono!!")
      #   return render(request, 'app/pagoCompletado.html')
      # else:
      #    print('El valor de resultado es : ',resultado)
    except Exception as e:
      print('no se encontro la venta',e)
    
    # Realizar la conexión a la base de datos Oracle
    # conn = cx_Oracle.connect('BASE_DATOS_CSHARP', '1234', 'localhost:1521/orcl')
    # cursor = conn.cursor()
    # # Declarar el cursor de salida para los resultados del procedimiento almacenado
    # datos = cursor.var(cx_Oracle.CURSOR)
    # # Ejecutar el procedimiento almacenado para buscar el despacho por ID
    # cursor.callproc('SP_BUSCAR_LIBRO', [id_libro,datos])
    # resultados = datos.getvalue().fetchall()
    # print("id_libro",resultados)
    
    # Obtener el resultado del cursor de salida
    # libro = datos.getvalue().fetchone()
    

    
    return render(request, 'app/catalogo.html', {'carrito': carrito.carrito, 'total': total})

def agregar_producto(request, libro_id):
    carrito = Carrito(request)
    carrito.agregar_producto(libro_id)
    return redirect('carrito')

def restar_producto(request, libro_id):
    carrito = Carrito(request)
    carrito.restar_producto(libro_id)
    return redirect('carrito')

def eliminar_producto(request, libro_id):
    carrito = Carrito(request)
    carrito.eliminar_producto(libro_id)
    return redirect('carrito')

def vaciar_carrito(request):
    carrito = Carrito(request)
    carrito.vaciar_carrito()
    return redirect('carrito')

def pagar(request):  
  return render(request, 'app/pagar_form.html')



#aqui se consume el servicio web
def pagoTarjeta(request):
    if request.method == 'POST':
        total_carrito = request.POST.get('total_carrito')
        mes_vencimiento = request.POST.get('mes_vencimiento')
        anio_vencimiento = request.POST.get('anio_vencimiento')
        p_fecha_vencimiento = f"{mes_vencimiento}/{anio_vencimiento}"
        p_num_tarjeta = request.POST.get('nroTarjeta')
        p_cvv = request.POST.get('cvv') 
        p_costo = total_carrito

        # Almacenar el valor de total_carrito en la sesión si está presente en la solicitud POST
        if total_carrito:
            request.session['total_carrito'] = total_carrito

        print("soy el carrito: ", total_carrito)
        print("soy el mes vencimiento: ", mes_vencimiento)
        print("soy el anio: ", anio_vencimiento)
        print("soy la fecha mas bonita: ", p_fecha_vencimiento)
        print("soy el num tarjeta", p_num_tarjeta)
        print("soy el cvv", p_cvv)
        print("soy el costo", p_costo)

        # Aquí puedes realizar el procesamiento necesario con los datos
        # Ejemplo de consumo del servicio web
        wsdl_url = 'http://localhost:8080/WsPago_de_una(G)/WsPago_de_una?WSDL'
        response = requests.get(wsdl_url)
        if response.status_code == 200:
            try:
                client = Client(wsdl_url)
                result = client.service.Pagar(p_num_tarjeta, p_cvv, p_fecha_vencimiento, p_costo)
                print("he llegado mamawebos")
                return redirect('pagoCompletado')
                

            except Exception as e:
                print("Error al consumir el servicio web de pago:", str(e))
                return render(request, 'app/pagoTarjeta.html')
        else:
            print("Error al acceder al servicio web de pago!")
            return render(request, 'app/Home.html')
    else:
        return render(request, 'app/pagoTarjeta.html')
   




def pagoCompletado(request):
  
   
    iva = 5888
    cliente_run = request.session.get('rut') 
    fecha = datetime.date.today()
    fecha_formateada = fecha.strftime("%d/%m/%y")
    tipo_venta = 20
    estado = 1
    trabajador_run = '11-1'
    total_carrito = 1250
    print(iva)
    print(cliente_run)
    print(fecha)
    print(tipo_venta)
    print(estado)
    print(trabajador_run)
    print(total_carrito)
    try:
      conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
      cursor = conn.cursor()
      # v_salida = cursor.var(cx_Oracle.STRING)
      cursor.callproc('SP_AGREGAR_VENTA', [fecha_formateada, total_carrito,iva,cliente_run,tipo_venta,estado,trabajador_run])
      # resultado = v_salida.getvalue()
      
      cursor.close()
      conn.commit()
      conn.close()
      
      # if resultado is not None:

      print("Funciono!!!")
      return render(request, 'app/pagoCompletado.html')
        
          # SUBTOTAL = total_carrito
          # SERVICIO_ID_SERVICIO = 0 
          # INSUMO_ID_INSUMO = 0 
          # LIBRO_ID_LIBRO = 0 
          # CANTIDAD = 1 
          # print(total_carrito)
          # conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
          # cursor = conn.cursor()
          # resp = cursor.var(cx_Oracle.CURSOR)
          # cursor.callproc('SP_ULTIMA_VENTA', resp)
          # resultados = resp.getvalue()
          # cursor.close()
          # conn.close()
          # VENTA_ID_VENTA =  resultados
          # if VENTA_ID_VENTA is not None :
          #    try:
          #       conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
          #       cursor = conn.cursor()
          #       respu = cursor.var(cx_Oracle.CURSOR)
          #       cursor.callproc('SP_AGREGAR_BOLETA', [SUBTOTAL, VENTA_ID_VENTA, SERVICIO_ID_SERVICIO, INSUMO_ID_INSUMO, LIBRO_ID_LIBRO, CANTIDAD, respu])
          #       cursor.close()
          #       conn.close()
          #       if respu is not None:
          #          print('He funcionado en generar una boleta')
          #          return render(request, 'app/pagoCompletado.html')
          #       else:  
          #          print('no he funcionado en generar una boleta')
          #    except Exception as e:
          #       print('no se encontro la venta',e) 
    #  else:
     #    print('El valor de resultado es : ',resultado)
    except Exception as e:
      print('no se encontro la venta',e)
      return render(request, 'app/pagoCompletado.html')

        
    return render(request, 'app/pagoCompletado.html')


def loginCliente(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        passw = request.POST.get('password')
        print('rut: ', rut)
        print('password',passw)
        try:
            conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
            cursor = conn.cursor()
            v_salida = cursor.var(cx_Oracle.STRING)
            cursor.callproc('SP_VALIDAR_CLIENTE', [rut, passw, v_salida])
            resultado = v_salida.getvalue()
            cursor.close()
            conn.close()
            
            if resultado is not None:
                print("Pase!")

                if resultado is not None:
                  print("pase resultado")
                  
                  messages.success(request, "Te has logueado correctamente")
                  request.session['rut'] = rut  # Almacena el valor del rut en la sesión
                  return render(request, 'app/home.html', {'resultado': resultado})
                else:
                  return HttpResponse("Credenciales inválidas")
            else:
                return HttpResponse("Credenciales inválidas")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            return HttpResponse(error.message)
    return render(request, 'app/login.html')
#aqui se consume el servicio web
# def despachoaWs(request):
#     if request.method == 'POST':
#        # Almacenar el valor de total_carrito en la sesión si está presente en la solicitud POST
#       p_direccion = request.POST.get('direccion')
#       p_telefono = request.POST.get('telefono')
#       comuna = request.POST.get('comuna')
#       # p_comuna = 
#       print(" Aqui vive el wn",p_direccion)
#       print("aqui hay que llamar al wn ",p_telefono)
#       print("la comuna del wn",p_comuna)

#         # Aquí puedes realizar el procesamiento necesario con los datos
#         # Ejemplo de consumo del servicio web
#       ws_url = 'http://localhost:8080/WsPago_de_una(G)/WsPago_de_una?WSDL'
#       response = requests.get(ws_url)
#       if response.status_code == 200:
#             try:
#                 client = Client(ws_url)
#                 result = client.service(p_num_tarjeta, p_cvv, p_fecha_vencimiento, p_costo)
#                 print("he llegado mamawebos")
#                 return render(request, 'app/pagoCompletado.html', {'result': result})
                
#             except Exception as e:
#                 print("Error al consumir el servicio web de pago:", str(e))
#                 return render(request, 'app/pagoTarjeta.html', {'error': True})
#       else:
#           return render(request, 'app/pagoTarjeta.html')

     #, {'form': form}

""" def login(request):
  return render(request, 'app/login.html') """


def catalogoInsumos(request):
    # Realizar la conexión a la base de datos Oracle
    conn = cx_Oracle.connect('BASE_DATOS_CSHARP', '1234', 'localhost:1521/orcl')
    cursor = conn.cursor()

    # Declarar el cursor de salida para los resultados del procedimiento almacenado
    Insumos = cursor.var(cx_Oracle.CURSOR)

    # Ejecutar el procedimiento almacenado
    cursor.callproc('SP_LISTAR_INSUMOS', [Insumos])

    # Obtener los resultados del cursor de salida
    resultados = Insumos.getvalue().fetchall()

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    # Pasar los resultados a la plantilla y renderizar la vista
    return render(request, 'app/catalogoinsumos.html', {'Insumos': resultados})

def quienesSomos(request):
  return render(request, 'app/quienesSomos.html')


def seguimiento(request):
    # ws_url = 'http://localhost:8080/WsSeguimiento(G)/wsSeguimiento?WSDL'
    
    # try:
    #   response = requests.get(ws_url)
      
    #   if response.status_code == 200:
    #     client = Client(ws_url)
    #     result = client.service.NuevoEstado()
    #     servicios = result['servicios']
    #     estados = [x['estado_id_estado'] for x in servicios]
        return render(request, 'app/seguimiento.html')
    #   else:
    #     print("Error con la conexion API")

    # except Exception as e:
    #     error_message = "Error al consumir el servicio web de seguimiento: " + str(e)
    #     return HttpResponse(error_message)

def reservas(request):
  return render(request, 'app/reservas.html')

def agendaLista(request):
  return render(request, 'app/agendaLista.html')

def agendaMenu(request):
  return render(request, 'app/agendaMenu.html')


def contacto(request):
  data = {
    'form': ContactoForm()
  }
  return render(request, 'app/contacto.html', data)

def despacho(request):
  return render(request, 'app/despacho.html')

def registroCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nombre_cli = form.cleaned_data['nombre_cli']
            apellido_cli = form.cleaned_data['apellido_cli']
            run = form.cleaned_data['run']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            direccion = form.cleaned_data['direccion']
            comuna_id_comuna = request.POST.get('comuna_id_comuna')  # Obtener el valor seleccionado del campo comuna_id_comuna
            contrasena = form.cleaned_data['contrasena']

            try:
              conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
              cursor = conn.cursor()
              cursor.callproc('SP_AGREGAR_CLIENTE', [nombre_cli, apellido_cli, run, email, telefono, direccion, comuna_id_comuna,contrasena ])
              cursor.close()
              conn.commit()
              conn.close()
              messages.success(request, "Cliente agregado correctamente")
              return render(request, 'app/home.html')
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                return HttpResponse(error.message)
    else:
        form = ClienteForm()

    return render(request, 'app/registroCliente.html', {'form': form})
      


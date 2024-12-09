import cx_Oracle

def obtener_nombres_comunas(id_comuna=None):
    conn = cx_Oracle.connect('BASE_DATOS_CSHARP/1234@localhost:1521/orcl')
    cursor = conn.cursor()
    try:
        # Crear cursor de salida para recuperar los resultados
        comuna_cursor = cursor.var(cx_Oracle.CURSOR)
        
        # Llamar al procedimiento almacenado para obtener los nombres de las comunas
        cursor.callproc('SP_BUSCAR_COMUNA', [id_comuna, comuna_cursor])
        
        # Recuperar el cursor de resultados
        comuna_result = comuna_cursor.getvalue()
        
        # Recuperar los resultados como una lista de tuplas
        results = [row for row in comuna_result]
        
        # Crear una lista de opciones para el combobox
        opciones = [(str(id_comuna), nombre_comuna) for id_comuna, nombre_comuna in results]
        
        return opciones
    finally:
        cursor.close()
        conn.close()
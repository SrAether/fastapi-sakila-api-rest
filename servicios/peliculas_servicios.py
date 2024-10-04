# .servicios/peliculas_servicios.py
# Creado por JOSE CARLOS TAPIA COBIAN
# CREADO PARA TAREA CREACION DE SERVICIOS USANDO FASTAPI
from db.conexion import Conexion

def obtener_pelicular_no_alquiladas_servicio():
    conexion = Conexion()
    peliculas = conexion.obtener_pelicular_no_alquiladas()
    return peliculas

def respaldar_peliculas_servicio(peliculas):
    """
    Respalda las películas seleccionadas en las tablas _backup.
    """
    # Crear una instancia de la clase Conexion
    conexion = Conexion()
    try:
        conexion.respaldar_peliculas(peliculas)
    except Exception as e:
        print(f"Error al respaldar las películas: {e}")
    finally:
        return "Respaldo exitoso"
    
    
def eliminar_peliculas_servicio( peliculas):
    """
    Elimina las películas seleccionadas y sus datos relacionados.
    """
    # Crear una instancia de la clase Conexion
    conexion = Conexion()
    try:
        conexion.eliminar_peliculas(peliculas)
    except Exception as e:
        print(f"Error al eliminar las películas: {e}")
    finally:
        return "Eliminación exitosa"
    

def obtener_actores_populares_servicio(cantidad: int = 10):
    """
    Obtiene los actores más populares según la cantidad especificada.
    """
    conexion = Conexion()
    try:
        actores = conexion.obtener_actores_populares(cantidad)
        return actores
    except Exception as e:
        return f"Error al obtener los actores populares: {e}"
    finally:
        conexion.close()
    
def actualizar_precio_peliculas_servicio():
    """
    Servicio para actualizar el precio de las películas.
    """
    conexion = Conexion()
    try:
        resumen = conexion.actualizar_precio_peliculas()
        return resumen
    except Exception as e:
        print(f"Error en el servicio de actualización de precios: {e}")
        raise  # Re-lanzar la excepción para que sea manejada en la capa superior

def obtener_peliculas_inactivas_detalle_servicio():
    conexion = Conexion()
    try:
        peliculas = conexion.obtener_peliculas_inactivas_detalle()
        return peliculas
    except Exception as e:
        print(f"Error en el servicio de obtener películas inactivas con detalle: {e}")
        raise
    
def obtener_respaldo_pelicula_servicio(pelicula_id: int):
    conexion = Conexion()
    try:
        pelicula = conexion.obtener_respaldo_pelicula(pelicula_id)
        return pelicula
    except Exception as e:
        print(f"Error en el servicio de obtener respaldo de película: {e}")
        raise
    
def obtener_historial_alquileres_servicio(pelicula_id: int):
    conexion = Conexion()
    try:
        historial = conexion.obtener_historial_alquileres(pelicula_id)
        return historial
    except Exception as e:
        print(f"Error en el servicio de obtener historial de alquileres: {e}")
        raise
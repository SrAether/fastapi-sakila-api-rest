# ./routers/peliculas_router.py
# Creado por JOSE CARLOS TAPIA COBIAN
# CREADO PARA TAREA CREACION DE SERVICIOS USANDO FASTAPI
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from servicios.peliculas_servicios import (
    respaldar_peliculas_servicio,
    eliminar_peliculas_servicio,
    obtener_pelicular_no_alquiladas_servicio,
    obtener_actores_populares_servicio,
    actualizar_precio_peliculas_servicio,
    obtener_peliculas_inactivas_detalle_servicio,
    obtener_respaldo_pelicula_servicio,
    obtener_historial_alquileres_servicio
)

router = APIRouter()

# Modelo para recibir los film_ids
class PeliculasSeleccionadas(BaseModel):
    peliculas_ids: List[int]

# 1. Obtener películas inactivas
@router.get("/peliculas_no_alquiladas")
def obtener_pelicular_no_alquiladas():
    peliculas = obtener_pelicular_no_alquiladas_servicio()
    if not peliculas:
        raise HTTPException(status_code=404, detail="No hay películas inactivas")
    return peliculas

# 2. Respaldar y eliminar películas seleccionadas
@router.delete("/peliculas/eliminar")
def eliminar_peliculas_seleccionadas(peliculas_seleccionadas: PeliculasSeleccionadas):
    # Obtener las películas inactivas
    peliculas_inactivas = obtener_pelicular_no_alquiladas_servicio()
    
    # Filtrar las películas seleccionadas por su film_id
    peliculas_filtradas = [
        pelicula for pelicula in peliculas_inactivas if pelicula.id_pelicula in peliculas_seleccionadas.peliculas_ids
    ]

    if not peliculas_filtradas:
        raise HTTPException(status_code=404, detail="No se encontraron películas para eliminar")

    # Respaldar las películas seleccionadas
    respaldo = respaldar_peliculas_servicio(peliculas=peliculas_filtradas)
    if respaldo != "Respaldo exitoso":
        raise HTTPException(status_code=500, detail="Error al realizar el respaldo")
    
    #return {"mensaje": "Peliculas seleccionadas: " + str(peliculas_seleccionadas.peliculas_ids)}

    # Eliminar las películas seleccionadas
    eliminacion = eliminar_peliculas_servicio(peliculas_filtradas)
    if eliminacion != "Eliminación exitosa":
        raise HTTPException(status_code=500, detail="Error al eliminar las películas")

    return {"mensaje": "Acción ejecutada correctamente"}



@router.get("/actores_populares")
def obtener_actores_populares(cantidad: int = 10):
    actores = obtener_actores_populares_servicio(cantidad)
    if not actores:
        raise HTTPException(status_code=404, detail="No hay actores populares")
    return actores

@router.put("/peliculas/actualizar_precios")
def actualizar_precios_peliculas():
    try:
        resumen = actualizar_precio_peliculas_servicio()
        return {"mensaje": "Precios actualizados correctamente", "resumen": resumen}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar los precios: {e}")
    
@router.get("/peliculas/inactivas")
def obtener_peliculas_inactivas_detalle():
    try:
        peliculas = obtener_peliculas_inactivas_detalle_servicio()
        return peliculas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las películas inactivas: {e}")


@router.get("/peliculas/{pelicula_id}/respaldo")
def obtener_respaldo_pelicula(pelicula_id: int):
    try:
        respaldo = obtener_respaldo_pelicula_servicio(pelicula_id)
        if not respaldo:
            raise HTTPException(status_code=404, detail="No se encontró un respaldo para esta película")
        return respaldo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el respaldo de la película: {e}")

@router.get("/peliculas/{pelicula_id}/historial")
def obtener_historial_alquileres(pelicula_id: int):
    try:
        historial = obtener_historial_alquileres_servicio(pelicula_id)
        return historial
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el historial de alquileres: {e}")

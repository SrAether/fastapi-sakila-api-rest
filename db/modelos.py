# ./db/modelos.py
# Creado por JOSE CARLOS TAPIA COBIAN
# CREADO PARA TAREA CREACION DE SERVICIOS USANDO FASTAPI
from pydantic import BaseModel
from datetime import datetime

class PeliculaBase(BaseModel):
    id_pelicula: int
    titulo: str
    tarifa_alquiler: float
    tiempo_alquiler: int
    ultima_actualizacion: datetime

    class Config:
        orm_mode = True  # Esto permite que FastAPI trabaje con clases ORM como las de SQLAlchemy si es necesario


class Pelicula:
    def __init__(self,
                 id_pelicula, 
                 titulo, 
                 tarifa_alquiler,
                 tiempo_alquiler,
                 ultima_actualizacion):
        self.id_pelicula = id_pelicula
        self.titulo = titulo
        self.tarifa_alquiler = tarifa_alquiler
        self.tiempo_alquiler = tiempo_alquiler
        self.ultima_actualizacion = ultima_actualizacion
    # Método para mostrar los datos de la película
    def __str__(self):
        return f"{self.id_pelicula} - {self.titulo} - {self.tarifa_alquiler} - {self.tiempo_alquiler} - {self.ultima_actualizacion}"
        
# main.py
# Creado por JOSE CARLOS TAPIA COBIAN
# CREADO PARA TAREA CREACION DE SERVICIOS USANDO FASTAPI
from fastapi import FastAPI
from routers.peliculas_router import router

app = FastAPI()

app.include_router(router)
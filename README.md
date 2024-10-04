
# Proyecto FastAPI: Servicios de Gestión de Películas

Este proyecto implementa una API de gestión de películas utilizando **FastAPI**. Permite realizar operaciones como obtener detalles de películas, respaldar y eliminar películas, gestionar actores populares, y actualizar precios de alquiler. Está diseñado para trabajar con una base de datos MySQL que utiliza el esquema **Sakila** y proporcionar servicios relacionados con películas y actores.

## Características

- **Obtener Películas No Alquiladas**: Recupera una lista de películas que no han sido alquiladas recientemente.
- **Respaldar y Eliminar Películas**: Permite respaldar películas seleccionadas y eliminarlas de la base de datos.
- **Obtener Actores Populares**: Devuelve una lista de los actores más populares.
- **Actualizar Precios de Películas**: Actualiza los precios de alquiler de las películas en la base de datos.
- **Obtener Detalles de Películas Inactivas**: Proporciona información detallada sobre películas que están inactivas.
- **Historial de Alquileres**: Recupera el historial de alquileres para una película específica.

## Estructura del Proyecto

\`\`\`plaintext
.
├── db
│   ├── conexion.py          # Maneja la conexión a la base de datos
│   ├── modelos.py           # Modelos para la estructura de datos
├── main.py                  # Archivo principal que ejecuta la aplicación FastAPI
├── routers
│   ├── peliculas_router.py   # Rutas de la API relacionadas con las películas
├── servicios
│   ├── peliculas_servicios.py  # Lógica de negocio para los servicios de películas
├── respaldos                # Carpeta para almacenar respaldos de datos
└── requisitos.txt           # Requerimientos de Python
\`\`\`

## Requisitos

Instala las dependencias necesarias utilizando el archivo \`requisitos.txt\`:

\`\`\`bash
pip install -r requisitos.txt
\`\`\`

### Dependencias principales:

- **FastAPI**: El framework web utilizado para crear la API.
- **PyMySQL**: Para la interacción con la base de datos MySQL o MariaDB.
- **Pillow**: Para manejar imágenes en caso de que se necesiten para la gestión de actores o películas.
- **Cryptography**: Proporciona seguridad adicional para la base de datos y las operaciones de la API.
- **JSONSchema**: Para validar la estructura de los datos que pasan por la API.

## Ejecución

Para iniciar la aplicación, ejecuta el siguiente comando:

\`\`\`bash
fastapi dev main.py
\`\`\`

Esto iniciará el servidor local de desarrollo de FastAPI y podrás acceder a la documentación interactiva en \`http://127.0.0.1:8000/docs\`.

## Endpoints Principales

- \`GET /peliculas_no_alquiladas\`: Recupera películas no alquiladas.
- \`DELETE /peliculas/eliminar\`: Respaldar y eliminar películas seleccionadas.
- \`GET /actores_populares\`: Obtener una lista de actores populares.
- \`PUT /peliculas/actualizar_precios\`: Actualiza los precios de alquiler de las películas.
- \`GET /peliculas/{pelicula_id}/respaldo\`: Obtener respaldo de una película.
- \`GET /peliculas/{pelicula_id}/historial\`: Obtener historial de alquileres de una película.

## Base de Datos

Este proyecto está diseñado para trabajar con una base de datos MySQL que utiliza el esquema **Sakila**. Asegúrate de configurar correctamente la conexión a la base de datos en \`db/conexion.py\`.

## Licencia

Este proyecto fue creado como parte de una tarea de **Creación de Servicios usando FastAPI** por **JOSE CARLOS TAPIA COBIAN**. Puedes modificarlo y distribuirlo según tus necesidades.

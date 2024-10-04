# ./db/conexion.py
# Creado por JOSE CARLOS TAPIA COBIAN
# CREADO PARA TAREA CREACION DE SERVICIOS USANDO FASTAPI
import pymysql
from datetime import datetime, timedelta
from db.modelos import Pelicula

class Conexion:
    def __init__(self):
        self.host = '192.168.122.227'
        self.port = 3306
        self.user = 'ajax'
        self.password = 'ajaxpassword'
        self.db = 'sakila'
        self.connection = None
        
    def open(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            ssl={'ssl': {'verify': False}}
        )
    
    def close(self):
        if self.connection and self.connection.open:
            self.connection.close()

        
    def obtener_pelicular_no_alquiladas(self):
        añoPasado = datetime.now() - timedelta(days=365)
        self.open()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                           SELECT film_id,
                                    title,
                                    rental_rate,
                                    rental_duration,
                                    last_update
                            FROM film
                            WHERE last_update < %s
                           """, (añoPasado))
            peliculas = cursor.fetchall()
        self.close()
        return [Pelicula(*pelicula) for pelicula in peliculas]
    
    def respaldar_peliculas(self, peliculas):
        """
        Respalda las películas seleccionadas en las tablas _backup.
        """
        self.open()
        try:
            with self.connection.cursor() as cursor:
                for pelicula in peliculas:
                    try:
                        cursor.execute("START TRANSACTION")

                        # Respaldar datos de la película
                        cursor.execute(
                            """
                            INSERT INTO sakila.film_backup
                            SELECT * FROM sakila.film
                            WHERE film_id = %s
                            """,
                            (pelicula.id_pelicula),
                        )
                        cursor.execute(
                            """
                            INSERT INTO sakila.film_actor_backup
                            SELECT * FROM sakila.film_actor
                            WHERE film_id = %s
                            """,
                            (pelicula.id_pelicula),
                        )
                        cursor.execute(
                            """
                            INSERT INTO sakila.film_category_backup
                            SELECT * FROM sakila.film_category
                            WHERE film_id = %s
                            """,
                            (pelicula.id_pelicula),
                        )
                        cursor.execute(
                            """
                            INSERT INTO sakila.inventory_backup
                            SELECT * FROM sakila.inventory
                            WHERE film_id = %s
                            """,
                            (pelicula.id_pelicula),
                        )
                        cursor.execute(
                            """
                            INSERT INTO sakila.rental_backup
                            SELECT r.* FROM sakila.rental r
                            JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
                            WHERE i.film_id = %s
                            """,
                            (pelicula.id_pelicula),
                        )

                        cursor.execute("COMMIT")
                    except Exception as e:
                        cursor.execute("ROLLBACK")
                        print(f"Error al respaldar la película {pelicula.id_pelicula}: {e}")
                        # Puedes devolver un mensaje de error o manejar la excepción de otra forma
        finally:
            self.close()

    def eliminar_peliculas(self, peliculas):
        """
        Elimina las películas seleccionadas y sus datos relacionados.
        """
        self.open()
        try:
            with self.connection.cursor() as cursor:
                for pelicula in peliculas:
                    try:
                        cursor.execute("START TRANSACTION")

                        # Eliminar la película y sus relaciones
                        cursor.execute(
                            "DELETE FROM rental WHERE inventory_id IN (SELECT inventory_id FROM inventory WHERE film_id = %s)",
                            (pelicula.id_pelicula)
                        )
                        cursor.execute("DELETE FROM film_actor WHERE film_id = %s", (pelicula.id_pelicula))
                        cursor.execute("DELETE FROM film_category WHERE film_id = %s", (pelicula.id_pelicula))
                        cursor.execute("DELETE FROM inventory WHERE film_id = %s", (pelicula.id_pelicula))
                        cursor.execute("DELETE FROM film WHERE film_id = %s", (pelicula.id_pelicula))

                        cursor.execute("COMMIT")
                    except Exception as e:
                        cursor.execute("ROLLBACK")
                        print(f"Error al eliminar la película {pelicula.id_pelicula}: {e}")
                        # Puedes devolver un mensaje de error o manejar la excepción de otra forma
        finally:
            self.close()
    
    
    def obtener_actores_populares(self, cantidad: int = 10):
        self.open()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                           SELECT a.actor_id, 
                                  a.first_name, 
                                  a.last_name, 
                                  COUNT(r.rental_id) AS total_alquileres
                           FROM actor a
                           JOIN film_actor fa ON a.actor_id = fa.actor_id
                           JOIN film f ON fa.film_id = f.film_id
                           JOIN inventory i ON f.film_id = i.film_id
                           JOIN rental r ON i.inventory_id = r.inventory_id
                           GROUP BY a.actor_id
                           ORDER BY total_alquileres DESC
                           LIMIT %s
                           """, (cantidad))
            actores = cursor.fetchall()
        self.close()
        return actores   
    
    def actualizar_precio_peliculas(self):
        """
        Actualiza el precio de alquiler de todas las películas basándose en su popularidad 
        (número de alquileres en los últimos 3 meses).
        """
        tres_meses_atras = datetime.now() - timedelta(days=90)
        self.open()
        try:
            with self.connection.cursor() as cursor:
                # Obtener la popularidad de cada película
                cursor.execute("""
                    SELECT f.film_id, COUNT(r.rental_id) AS total_alquileres
                    FROM film f
                    JOIN inventory i ON f.film_id = i.film_id
                    JOIN rental r ON i.inventory_id = r.inventory_id
                    WHERE r.rental_date >= %s
                    GROUP BY f.film_id
                """, (tres_meses_atras,))
                peliculas_rentadas = cursor.fetchall()

                resumen_actualizaciones = []
                for pelicula_id, total_alquileres in peliculas_rentadas:
                    if total_alquileres > 100:
                        precio = 4.99
                    elif total_alquileres >= 50:
                        precio = 3.99
                    elif total_alquileres >= 20:
                        precio = 2.99
                    else:
                        precio = 1.99

                    # Actualizar el precio de la película
                    cursor.execute("UPDATE film SET rental_rate = %s WHERE film_id = %s", (precio, pelicula_id))
                    resumen_actualizaciones.append({"film_id": pelicula_id, "nuevo_precio": precio})

                self.connection.commit()
                return resumen_actualizaciones
        except Exception as e:
            self.connection.rollback()
            print(f"Error al actualizar los precios de las películas: {e}")
            raise  # Re-lanzar la excepción para que sea manejada en la capa superior
        finally:
            self.close()
            
            
    def obtener_peliculas_inactivas_detalle(self):
        añoPasado = datetime.now() - timedelta(days=365)
        self.open()
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        f.film_id, 
                        f.title, 
                        f.description, 
                        f.release_year, 
                        f.language_id, 
                        f.original_language_id, 
                        f.rental_duration, 
                        f.rental_rate, 
                        f.length, 
                        f.replacement_cost, 
                        f.rating, 
                        f.special_features,
                        GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actores,
                        GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categorias
                    FROM film f
                    LEFT JOIN film_actor fa ON f.film_id = fa.film_id
                    LEFT JOIN actor a ON fa.actor_id = a.actor_id
                    LEFT JOIN film_category fc ON f.film_id = fc.film_id
                    LEFT JOIN category c ON fc.category_id = c.category_id
                    LEFT JOIN inventory i ON f.film_id = i.film_id
                    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
                    WHERE r.rental_date < %s OR r.rental_date IS NULL
                    GROUP BY f.film_id
                """, (añoPasado,))
                peliculas = cursor.fetchall()
                return peliculas
        except Exception as e:
            print(f"Error al obtener detalles de películas inactivas: {e}")
            raise
        finally:
            self.close()


    def obtener_respaldo_pelicula(self, pelicula_id):
        self.open()
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:  # Corrección: faltaba 'as cursor'
                cursor.execute("""
                    SELECT * 
                    FROM film_backup 
                    WHERE film_id = %s
                """, (pelicula_id,))
                pelicula = cursor.fetchone()
                return pelicula
        except Exception as e:
            print(f"Error al obtener el respaldo de la película {pelicula_id}: {e}")
            raise
        finally:
            self.close()

    def obtener_historial_alquileres(self, pelicula_id):
        self.open()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT r.rental_date, r.return_date, c.first_name, c.last_name
                    FROM rental r
                    JOIN inventory i ON r.inventory_id = i.inventory_id
                    JOIN customer c ON r.customer_id = c.customer_id
                    WHERE i.film_id = %s
                """, (pelicula_id,))
                historial = cursor.fetchall()
                return historial
        except Exception as e:
            print(f"Error al obtener el historial de alquileres de la película {pelicula_id}: {e}")
            raise
        finally:
            self.close()
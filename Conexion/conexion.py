import os
import mysql.connector
from mysql.connector import Error, pooling


# Configuración de parámetros mediante variables de entorno (con fallback a valores locales)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "256323890"),
    "database": os.getenv("DB_NAME", "panaderia_cozi"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Crear un Pool de Conexiones para reutilizar recursos
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="panaderia_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
except Error as e:
    print(f"[Error Crítico] No se pudo inicializar el pool de conexiones: {e}")
    connection_pool = None


def conectar():
    """
    Obtiene una conexión desde el pool si está disponible,
    o intenta una conexión directa como respaldo.
    """
    if connection_pool:
        try:
            return connection_pool.get_connection()
        except Error as e:
            print(f"[Error Pool] No se pudo obtener conexión del pool: {e}")

    # Respaldo en caso de que el pool falle o no esté inicializado
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"[Error Base de Datos] Imposible conectar a MySQL: {e}")
    return None


class ConexionDB:
    """
    Context Manager para asegurar el cierre automático de conexiones y cursores.
    Uso:
        with ConexionDB() as (conexion, cursor):
            cursor.execute("SELECT...")
    """
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def __enter__(self):
        self.conexion = conectar()
        if not self.conexion:
            raise Error("No hay conexión disponible con la base de datos.")
        self.cursor = self.conexion.cursor()
        return self.conexion, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conexion and self.conexion.is_connected():
            if exc_type is not None:
                self.conexion.rollback()  # Revierte si hubo un error
            else:
                self.conexion.commit()    # Confirma si todo salió bien
            self.conexion.close()
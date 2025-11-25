"""
Script para crear la base de datos PostgreSQL
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración de la conexión
DB_CONFIG = {
    'dbname': 'postgres',  # Conectar a la base de datos por defecto
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

NEW_DB_NAME = 'gestion_salud_db'

try:
    # Conectar a la base de datos postgres
    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Verificar si la base de datos existe
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (NEW_DB_NAME,))
    exists = cursor.fetchone()
    
    if exists:
        print(f"La base de datos '{NEW_DB_NAME}' ya existe. Eliminándola...")
        # Terminar conexiones activas
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{NEW_DB_NAME}'
            AND pid <> pg_backend_pid();
        """)
        # Eliminar la base de datos
        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(NEW_DB_NAME)))
        print(f"Base de datos '{NEW_DB_NAME}' eliminada.")
    
    # Crear la base de datos con codificación UTF8
    cursor.execute(sql.SQL(
        "CREATE DATABASE {} WITH ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0"
    ).format(sql.Identifier(NEW_DB_NAME)))
    
    print(f"✓ Base de datos '{NEW_DB_NAME}' creada exitosamente con codificación UTF8")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"Error al crear la base de datos: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

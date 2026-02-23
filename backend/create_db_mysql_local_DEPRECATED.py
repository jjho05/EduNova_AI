"""
Script para crear la base de datos MySQL
"""
import pymysql

# Configuración
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # Cambia si tienes password
DB_NAME = "educativo_db"

try:
    # Conectar a MySQL (sin especificar base de datos)
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    cursor = connection.cursor()
    
    # Crear base de datos si no existe
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print(f"✅ Base de datos '{DB_NAME}' creada/verificada exitosamente")
    
    cursor.close()
    connection.close()
    
    print("\n🎉 ¡Listo! Ahora puedes ejecutar:")
    print("   uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Asegúrate de que MySQL esté corriendo:")
    print("   - En Mac: brew services start mysql")
    print("   - O usa XAMPP/MAMP")

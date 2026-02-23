# 🎯 Configuración Rápida con MySQL Workbench

Ya tienes MySQL Workbench instalado, ¡perfecto! Vamos a configurarlo:

## Paso 1: Verificar que MySQL esté corriendo

Abre MySQL Workbench y verifica que tengas una conexión activa (generalmente "Local instance MySQL").

## Paso 2: Crear la base de datos

### Opción A: Desde MySQL Workbench (Visual)

1. Abre MySQL Workbench
2. Conecta a tu instancia local
3. En el menú, click en "Database" → "Create Schema"
4. Nombre: `educativo_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

### Opción B: Desde la terminal (Más rápido)

```bash
# Conectar a MySQL (te pedirá password si lo configuraste)
mysql -u root -p

# Dentro de MySQL, ejecutar:
CREATE DATABASE educativo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

## Paso 3: Actualizar .env si tienes password

Si tu MySQL tiene password, actualiza el archivo `.env`:

```
DATABASE_URL=mysql+pymysql://root:TU_PASSWORD@localhost:3306/educativo_db
```

Si NO tiene password (como está ahora):
```
DATABASE_URL=mysql+pymysql://root:@localhost:3306/educativo_db
```

## Paso 4: Probar la conexión

```bash
cd backend
source venv/bin/activate
python create_db.py
```

Si ves "✅ Base de datos 'educativo_db' creada/verificada exitosamente", ¡listo!

## Paso 5: Ejecutar el backend

```bash
uvicorn app.main:app --reload
```

Luego abre: http://localhost:8000/docs

---

## 💡 Tip: Ver las tablas en MySQL Workbench

Después de ejecutar el backend por primera vez:
1. En MySQL Workbench, actualiza (F5)
2. Expande `educativo_db` → `Tables`
3. Deberías ver: `users`, `courses`, `quizzes`

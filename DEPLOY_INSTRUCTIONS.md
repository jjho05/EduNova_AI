# 🚀 DEPLOY A HUGGING FACE SPACES + SUPABASE

## ✅ Todo Listo para Deploy

Tu proyecto ha sido completamente preparado para desplegarse en Hugging Face Spaces con base de datos PostgreSQL en Supabase (100% gratis).

---

## 📋 PASO A PASO

### 1️⃣ Crear Base de Datos en Supabase (5 minutos)

1. Ve a https://supabase.com
2. Haz clic en **"Start your project"**
3. Inicia sesión con GitHub
4. Crea un **New project**:
   - **Name**: `educativo-db` (o el que prefieras)
   - **Database Password**: Guarda esta contraseña (la necesitarás)
   - **Region**: Elige el más cercano a ti
   - Clic en **"Create new project"**

5. Espera 2-3 minutos mientras Supabase crea tu base de datos

6. Cuando esté listo, ve a **Settings** → **Database**

7. Busca la sección **Connection string** y selecciona el modo **URI**

8. Copia la URL completa que se ve así:
   ```
   postgresql://postgres.xxxx:[YOUR-PASSWORD]@xxxx.supabase.co:5432/postgres
   ```

9. **Reemplaza** `[YOUR-PASSWORD]` con la contraseña que guardaste en el paso 4

---

### 2️⃣ Obtener API Key de Google Gemini (2 minutos)

1. Ve a https://makersuite.google.com/app/apikey

2. Inicia sesión con tu cuenta de Google

3. Haz clic en **"Create API Key"**

4. Selecciona un proyecto de Google Cloud (o crea uno nuevo)

5. Copia la API Key generada

---

### 3️⃣ Crear Hugging Face Space (10 minutos)

1. Ve a https://huggingface.co/spaces

2. Haz clic en **"Create new Space"**

3. Configuración del Space:
   - **Owner**: Tu usuario
   - **Space name**: `generador-educativo-ia` (o el que prefieras)
   - **License**: MIT
   - **Select the Space SDK**: **Docker**
   - **Space hardware**: **CPU basic** (gratis)
   - Haz clic en **"Create Space"**

4. Una vez creado, ve a **Settings** en tu Space

5. En la sección **"Variables and secrets"**, agrega estos 3 secrets:

   **Secret 1:**
   - Name: `DATABASE_URL`
   - Value: La URL de Supabase que copiaste (completa con la password)
   
   **Secret 2:**
   - Name: `GEMINI_API_KEY`
   - Value: La API Key de Google que copiaste
   
   **Secret 3:**
   - Name: `SECRET_KEY`
   - Value: Cualquier texto largo y aleatorio (ej: `mi_super_secret_key_123456789_muy_seguro`)

6. Guarda los secrets

---

### 4️⃣ Subir el Código a Hugging Face

**Opción A: Desde Terminal (Recomendada)**

```bash
# Navegar a la carpeta del backend
cd "PROYECTO MULTIPLATAFORMA IA/backend"

# Inicializar git (si no está inicializado)
git init

# Agregar el remote de Hugging Face
# Reemplaza TU_USUARIO y TU_SPACE_NAME con tus datos
git remote add space https://huggingface.co/spaces/TU_USUARIO/TU_SPACE_NAME

# Agregar todos los archivos
git add .

# Crear commit
git commit -m "Deploy inicial: Backend + Frontend integrado"

# Subir a Hugging Face
git push --force space main
```

**Opción B: Desde la Web de Hugging Face**

1. En tu Space, ve a la pestaña **Files**
2. Arrastra y suelta estos archivos/carpetas desde `backend/`:
   - `app/` (carpeta completa)
   - `static/` (carpeta completa)
   - `uploads/` (carpeta completa)
   - `Dockerfile`
   - `start.sh`
   - `requirements.txt`
   - `seed_data.py`
   - `README.md`

---

### 5️⃣ Verificar el Deploy

1. Espera 5-10 minutos mientras Hugging Face construye el Docker container

2. Verás un log en tiempo real. Busca estos mensajes:
   ```
   🚀 Iniciando aplicación en Hugging Face Spaces...
   📊 Creando/actualizando tablas en PostgreSQL...
   ✅ Tablas creadas/verificadas
   🌱 Verificando si necesita datos iniciales...
   🔥 Iniciando servidor FastAPI en puerto 7860...
   ```

3. Cuando veas `Application startup complete`, tu app está lista

4. Haz clic en el botón **"Open"** o visita la URL de tu Space

---

## 🎉 ¡Listo!

Tu aplicación ya está en vivo. Puedes:

1. **Acceder a la app**: https://tuusuario-tu-space-name.hf.space
2. **Ver la API**: https://tuusuario-tu-space-name.hf.space/docs

### 👤 Credenciales de Prueba

**Profesor:**
- Email: `profesor@test.com`
- Password: `profesor123`

**Alumnos:**
- Email: `maria@test.com` | Password: `alumno123`
- Email: `carlos@test.com` | Password: `alumno123`
- Email: `ana@test.com` | Password: `alumno123`

---

## 🔧 Troubleshooting

### Error: "Database connection failed"
- Verifica que la `DATABASE_URL` en los secrets sea correcta
- Asegúrate de haber reemplazado `[YOUR-PASSWORD]` con tu contraseña real

### Error: "Gemini API error"
- Verifica que la `GEMINI_API_KEY` sea correcta
- Asegúrate de tener cuota disponible en Google AI Studio

### El Space se reinicia constantemente
- Revisa los logs en la pestaña **"Logs"** del Space
- Verifica que los 3 secrets estén configurados correctamente

---

## 📊 Recursos Incluidos

- ✅ Backend FastAPI con PostgreSQL
- ✅ Frontend Flutter Web integrado
- ✅ Base de datos auto-poblada con datos de prueba
- ✅ API documentada en `/docs`
- ✅ Autenticación JWT
- ✅ Integración con Google Gemini
- ✅ Upload de archivos
- ✅ Dashboard de progreso en tiempo real

---

**¿Listo para hacer deploy?** Sigue los pasos en orden y tendrás tu app en línea en menos de 20 minutos.

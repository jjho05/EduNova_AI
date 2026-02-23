# 🎯 Guía de Inicio Rápido

## Para Empezar HOY

### 1. MySQL (5 minutos)

Abre MySQL Workbench y ejecuta:
```sql
CREATE DATABASE educativo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend (2 minutos)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Abre: http://localhost:8000/docs

### 3. Flutter (5 minutos)

```bash
# Si no has creado el proyecto
flutter create frontend_flutter
cp -r flutter_code/* frontend_flutter/lib/
cp flutter_code/pubspec.yaml frontend_flutter/

cd frontend_flutter
flutter pub get
flutter run -d chrome
```

## Probar la App

1. **Registrarse**
   - Abre http://localhost:XXXX (Flutter te dirá el puerto)
   - Click en "Regístrate"
   - Llena el formulario
   - Selecciona "Profesor" o "Estudiante"

2. **Crear un Curso** (como Profesor)
   - Dashboard → "Mis Cursos"
   - Click en "Crear Curso"
   - Título: "Cálculo Diferencial"
   - Click en "Generar con IA"
   - ¡Espera unos segundos!

3. **Ver el Curso**
   - Aparecerá en tu lista
   - Click para ver detalles

## Problemas Comunes

### MySQL no conecta
```bash
# Verifica que MySQL esté corriendo
# En MySQL Workbench, verifica la conexión
```

### Flutter no encuentra dependencias
```bash
cd frontend_flutter
flutter clean
flutter pub get
```

### Backend da error
```bash
# Verifica que el venv esté activado
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

## Siguiente Paso

Una vez que funcione, podemos:
1. Agregar más funcionalidades
2. Crear el bot de Discord
3. Desplegar en producción

---

**¿Listo para probar?** 🚀

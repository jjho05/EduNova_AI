---
title: Generador Educativo IA
emoji: 🎓
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🎓 Generador de Contenido Educativo Inteligente

Plataforma educativa multiplataforma con IA generativa (Google Gemini) para crear cursos, quizzes, cronogramas y rúbricas automáticamente.

## ✨ Características

- 🤖 **IA Generativa**: Crea contenido educativo con Google Gemini
- 📚 **Gestión de Cursos**: Crea y administra cursos completos
- 📝 **Quizzes Inteligentes**: Generación automática de evaluaciones
- 📊 **Seguimiento de Progreso**: Dashboard en tiempo real
- 👥 **Roles**: Profesor y Alumno con permisos diferenciados
- 📱 **Multiplataforma**: Web, Android, iOS

## 🚀 Configuración en Hugging Face Spaces

### 1. Crear Base de Datos en Supabase

1. Ve a [Supabase](https://supabase.com) y crea una cuenta gratuita
2. Crea un nuevo proyecto
3. Ve a **Settings** → **Database** 
4. Copia la **Connection String** (formato: `postgresql://...`)

### 2. Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una API Key
3. Cópiala

### 3. Configurar Secrets en Hugging Face

En tu Space, ve a **Settings** → **Variables and secrets** y agrega:

```
DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:[PORT]/postgres
GEMINI_API_KEY=tu_api_key_aqui
SECRET_KEY=un_string_secreto_aleatorio_muy_largo
```

**Ejemplo de DATABASE_URL de Supabase:**
```
postgresql://postgres.xxxxxxxxxxxx:your-password@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

### 4. Deploy

Una vez configurados los secrets, el Space se reiniciará automáticamente y:

1. ✅ Creará las tablas en PostgreSQL
2. ✅ Poblará con datos de prueba (usuarios, cursos)
3. ✅ Estará listo para usar

## 👤 Credenciales de Prueba

### Profesor
- **Email**: profesor@test.com
- **Password**: profesor123

### Alumnos
- **Email**: maria@test.com | **Password**: alumno123
- **Email**: carlos@test.com | **Password**: alumno123
- **Email**: ana@test.com | **Password**: alumno123

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Flutter Web
- **IA**: Google Gemini 1.5 Flash
- **Auth**: JWT
- **Deploy**: Docker en Hugging Face Spaces

## 📝 Licencia

MIT

## 🤝 Créditos

Desarrollado con Antigravity Architect

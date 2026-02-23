#!/bin/bash

echo "🎓 Configuración del Sistema Educativo con IA"
echo "=============================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Backend Setup
echo -e "${BLUE}📦 Configurando Backend...${NC}"
cd backend

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Configurar .env
if [ ! -f ".env" ]; then
    echo "Creando archivo .env..."
    cp .env.example .env
    echo -e "${RED}⚠️  IMPORTANTE: Edita backend/.env con tus credenciales${NC}"
fi

echo -e "${GREEN}✅ Backend configurado${NC}"
echo ""

# 2. Base de Datos
echo -e "${BLUE}🗄️  Configurando Base de Datos...${NC}"
echo "Asegúrate de tener MySQL instalado y corriendo"
echo "Ejecuta manualmente:"
echo "  mysql -u root -p"
echo "  CREATE DATABASE educativo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "  exit;"
echo ""

# 3. Frontend Setup
echo -e "${BLUE}📱 Configurando Frontend...${NC}"
cd ../frontend_flutter

# Instalar dependencias
echo "Instalando dependencias de Flutter..."
flutter pub get

echo -e "${GREEN}✅ Frontend configurado${NC}"
echo ""

# 4. Instrucciones finales
echo -e "${GREEN}🎉 Configuración completa!${NC}"
echo ""
echo "Para ejecutar el proyecto:"
echo ""
echo "1. Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Frontend (en otra terminal):"
echo "   cd frontend_flutter"
echo "   flutter run -d chrome"
echo ""
echo "3. Acceder:"
echo "   Backend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: http://localhost:PORT"
echo ""
echo -e "${RED}⚠️  No olvides configurar GEMINI_API_KEY en backend/.env${NC}"

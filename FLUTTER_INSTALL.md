# 🚀 Instalación de Flutter

## Opción 1: Homebrew (Recomendado para Mac)

```bash
# Instalar Flutter
brew install --cask flutter

# Verificar instalación
flutter doctor

# Aceptar licencias de Android
flutter doctor --android-licenses

# Habilitar web
flutter config --enable-web
```

## Opción 2: Descarga Manual

1. Descargar: https://docs.flutter.dev/get-started/install/macos
2. Extraer el archivo
3. Agregar al PATH en `~/.zshrc`:
```bash
export PATH="$PATH:/ruta/a/flutter/bin"
```
4. Ejecutar `flutter doctor`

## Después de instalar:

```bash
# Verificar
flutter doctor

# Crear proyecto
cd "PROYECTO MULTIPLATAFORMA IA"
flutter create frontend_flutter

# Ejecutar en web
cd frontend_flutter
flutter run -d chrome
```

## ⏱️ Tiempo estimado: 10-15 minutos

Mientras se instala, podemos:
1. Diseñar la estructura del proyecto
2. Planificar las pantallas
3. Ver ejemplos de código

**¿Quieres que instalemos Flutter ahora o prefieres que diseñemos la estructura primero?**

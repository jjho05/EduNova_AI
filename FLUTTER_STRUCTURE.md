# 📱 Estructura del Proyecto Flutter

## Diseño de Pantallas

### 🔐 Autenticación
```
lib/screens/auth/
├── login_screen.dart       # Pantalla de login
├── register_screen.dart    # Pantalla de registro
└── onboarding_screen.dart  # Tutorial inicial (opcional)
```

### 👨‍🏫 Dashboard Profesor
```
lib/screens/teacher/
├── teacher_dashboard.dart          # Dashboard principal
├── courses/
│   ├── courses_list_screen.dart    # Mis cursos
│   ├── create_course_screen.dart   # Crear curso
│   ├── course_detail_screen.dart   # Detalle del curso
│   └── upload_curriculum_screen.dart # Subir retícula
├── assignments/
│   ├── create_assignment_screen.dart # Crear tarea/examen
│   └── assignments_list_screen.dart  # Lista de tareas
├── analytics/
│   └── analytics_screen.dart       # Estadísticas y gráficas
└── students/
    └── students_list_screen.dart   # Lista de alumnos
```

### 👨‍🎓 Dashboard Alumno
```
lib/screens/student/
├── student_dashboard.dart      # Dashboard principal
├── my_courses_screen.dart      # Mis cursos
├── quiz_screen.dart            # Realizar quiz
├── assignments_screen.dart     # Ver tareas
├── progress_screen.dart        # Mi progreso
└── chat_screen.dart            # Chat con IA
```

### 🧩 Widgets Reutilizables
```
lib/widgets/
├── common/
│   ├── custom_button.dart
│   ├── custom_text_field.dart
│   ├── loading_indicator.dart
│   └── error_message.dart
├── charts/
│   ├── progress_chart.dart     # Gráfica de progreso
│   ├── comparison_chart.dart   # Gráfica comparativa
│   └── pie_chart.dart          # Gráfica de pastel
└── cards/
    ├── course_card.dart
    ├── assignment_card.dart
    └── student_card.dart
```

### 🔧 Servicios
```
lib/services/
├── api_service.dart        # Conexión con backend
├── auth_service.dart       # Autenticación
├── storage_service.dart    # Almacenamiento local
└── notification_service.dart # Notificaciones
```

### 📦 Modelos
```
lib/models/
├── user.dart
├── course.dart
├── quiz.dart
├── assignment.dart
└── progress.dart
```

### 🎨 Tema y Configuración
```
lib/config/
├── theme.dart          # Tema de la app
├── routes.dart         # Rutas
└── constants.dart      # Constantes
```

## 🎨 Paleta de Colores (Propuesta)

```dart
// lib/config/theme.dart
class AppColors {
  static const primary = Color(0xFF6366F1);      // Indigo
  static const secondary = Color(0xFF8B5CF6);    // Purple
  static const success = Color(0xFF10B981);      // Green
  static const warning = Color(0xFFF59E0B);      // Amber
  static const error = Color(0xFFEF4444);        // Red
  static const background = Color(0xFFF9FAFB);   // Gray 50
  static const surface = Color(0xFFFFFFFF);      // White
  static const textPrimary = Color(0xFF111827);  // Gray 900
  static const textSecondary = Color(0xFF6B7280); // Gray 500
}
```

## 📱 Flujo de Navegación

```
Splash Screen
    ↓
Login/Register
    ↓
    ├─→ Profesor Dashboard
    │       ├─→ Mis Cursos
    │       ├─→ Crear Curso
    │       ├─→ Estadísticas
    │       └─→ Alumnos
    │
    └─→ Alumno Dashboard
            ├─→ Mis Cursos
            ├─→ Realizar Quiz
            ├─→ Mi Progreso
            └─→ Chat IA
```

## 🔌 Dependencias Principales

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Estado
  provider: ^6.1.0
  
  # Networking
  dio: ^5.4.0
  
  # Almacenamiento
  flutter_secure_storage: ^9.0.0
  shared_preferences: ^2.2.2
  
  # Routing
  go_router: ^13.0.0
  
  # UI
  google_fonts: ^6.1.0
  
  # Gráficas
  fl_chart: ^0.66.0
  
  # PDFs
  file_picker: ^6.1.1
  pdf: ^3.10.7
  
  # Utilidades
  intl: ^0.19.0
```

## 🎯 Prioridades de Desarrollo

### Semana 1 (Esta semana):
1. ✅ Setup proyecto Flutter
2. ✅ Configurar tema
3. ✅ Login/Register screens
4. ✅ Conexión con backend

### Semana 2:
1. Dashboard profesor
2. Crear curso
3. Lista de cursos

### Semana 3:
1. Dashboard alumno
2. Quiz screen
3. Progreso

**¿Te gusta esta estructura? ¿Quieres cambiar algo antes de empezar?**

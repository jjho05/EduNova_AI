import 'package:go_router/go_router.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/teacher/teacher_dashboard.dart';
import '../screens/teacher/courses_list_screen.dart';
import '../screens/teacher/create_course_screen.dart';
import '../screens/student/student_dashboard.dart';
import '../screens/common/notifications_screen.dart';
import '../screens/common/chat_screen.dart';
import '../screens/student/progress_screen.dart';
import '../screens/common/course_detail_screen.dart';
import '../screens/common/upload_document_screen.dart';
import '../screens/student/quiz_screen.dart';
import '../screens/teacher/quiz_statistics_screen.dart';

class AppRouter {
  static final router = GoRouter(
    initialLocation: '/login',
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/teacher',
        builder: (context, state) => const TeacherDashboard(),
      ),
      GoRoute(
        path: '/teacher/courses',
        builder: (context, state) => const CoursesListScreen(),
      ),
      GoRoute(
        path: '/teacher/create-course',
        builder: (context, state) => const CreateCourseScreen(),
      ),
      GoRoute(
        path: '/student',
        builder: (context, state) => const StudentDashboard(),
      ),
      GoRoute(
        path: '/notifications',
        builder: (context, state) => const NotificationsScreen(),
      ),
      GoRoute(
        path: '/chat',
        builder: (context, state) => const ChatScreen(),
      ),
      GoRoute(
        path: '/progress',
        builder: (context, state) => const ProgressScreen(),
      ),
      GoRoute(
        path: '/course/:id',
        builder: (context, state) {
          final courseId = state.pathParameters['id']!;
          return CourseDetailScreen(courseId: courseId);
        },
      ),
      GoRoute(
        path: '/upload-document',
        builder: (context, state) {
          final courseId = state.uri.queryParameters['courseId'];
          return UploadDocumentScreen(courseId: courseId);
        },
      ),
      GoRoute(
        path: '/quiz/:id',
        builder: (context, state) {
          final quizId = state.pathParameters['id']!;
          final quizTitle = state.uri.queryParameters['title'] ?? 'Quiz';
          return QuizScreen(quizId: quizId, quizTitle: quizTitle);
        },
      ),
      GoRoute(
        path: '/quiz/:id/statistics',
        builder: (context, state) {
          final quizId = state.pathParameters['id']!;
          final quizTitle = state.uri.queryParameters['title'] ?? 'Quiz';
          return QuizStatisticsScreen(quizId: quizId, quizTitle: quizTitle);
        },
      ),
    ],
  );
}

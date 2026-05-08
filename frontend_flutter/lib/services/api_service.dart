import 'dart:convert';
import 'package:dio/dio.dart';
import '../config/constants.dart';
import 'storage_service.dart';
import '../models/course.dart';
import '../models/assignment.dart';
import '../models/notification.dart' as model;
import 'package:file_picker/file_picker.dart';

class ApiService {
  late Dio _dio;
  final StorageService _storage = StorageService();

  ApiService() {
    _dio = Dio(BaseOptions(
      baseUrl: AppConstants.apiBaseUrl,
      connectTimeout: AppConstants.connectionTimeout,
      receiveTimeout: AppConstants.receiveTimeout,
      headers: {
        'Content-Type': 'application/json',
      },
    ));

    // Add interceptor for auth token
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _storage.getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
    ));
  }

  // Auth
  Future<Map<String, dynamic>> register(
      String email, String name, String password, String role) async {
    final response = await _dio.post('/auth/register', data: {
      'email': email,
      'name': name,
      'password': password,
      'role': role,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await _dio.get('/users/me');
    return response.data;
  }

  // Courses
  Future<List<Course>> getCourses() async {
    final response = await _dio.get('/courses');
    dynamic rawData = response.data;

    // If Dio returned a String, decode it manually
    if (rawData is String) {
      rawData = jsonDecode(rawData);
    }

    if (rawData is List) {
      return rawData
          .map((json) => Course.fromJson(Map<String, dynamic>.from(json)))
          .toList();
    }

    return [];
  }

  Future<Course> createCourse(String title, String? description) async {
    final response = await _dio.post('/courses', data: {
      'title': title,
      'description': description,
    });
    return Course.fromJson(response.data);
  }

  Future<void> deleteCourse(String courseId) async {
    await _dio.delete('/courses/$courseId');
  }

  Future<Course> getCourse(String courseId) async {
    final response = await _dio.get('/courses/$courseId');
    return Course.fromJson(response.data);
  }

  // Quizzes
  Future<Map<String, dynamic>> generateTopicQuiz(
      String topic, int numQuestions) async {
    final response = await _dio.post('/quizzes/topic', data: {
      'topic': topic,
      'num_preguntas': numQuestions,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> generateLevelingQuiz() async {
    final response = await _dio.post('/quizzes/leveling');
    return response.data;
  }

  // AI Chat
  Future<String> chatWithAI(String message) async {
    final response = await _dio.post('/ai/chat', data: {
      'message': message,
    });
    return response.data['response'];
  }

  // Assignments
  Future<List<Assignment>> getCourseAssignments(String courseId) async {
    final response = await _dio.get('/assignments/course/$courseId');
    return (response.data as List)
        .map((json) => Assignment.fromJson(json))
        .toList();
  }

  Future<List<Submission>> getMySubmissions() async {
    final response = await _dio.get('/my-submissions');
    return (response.data as List)
        .map((json) => Submission.fromJson(json))
        .toList();
  }

  Future<void> submitAssignment(
      String assignmentId, String? content, PlatformFile? file) async {
    if (file != null) {
      // Upload with file (Cross-platform)
      FormData formData = FormData.fromMap({
        'assignment_id': assignmentId,
        if (content != null) 'content': content,
        'file': MultipartFile.fromBytes(
          file.bytes!,
          filename: file.name,
        ),
      });
      await _dio.post('/submissions', data: formData);
    } else {
      // Upload without file
      await _dio.post('/submissions', data: {
        'assignment_id': assignmentId,
        'content': content,
      });
    }
  }

  // Notifications
  Future<List<model.Notification>> getNotifications(
      {bool unreadOnly = false}) async {
    final response = await _dio.get('/notifications', queryParameters: {
      'unread_only': unreadOnly,
    });
    return (response.data as List)
        .map((json) => model.Notification.fromJson(json))
        .toList();
  }

  Future<void> markNotificationRead(String notificationId) async {
    await _dio.patch('/notifications/$notificationId', data: {
      'is_read': true,
    });
  }

  Future<void> markAllNotificationsRead() async {
    await _dio.post('/notifications/mark-all-read');
  }

  // Documents
  Future<Map<String, dynamic>> uploadDocument({
    required List<int> fileBytes,
    required String fileName,
    required String name,
    String? description,
    required String documentType,
    String? courseId,
  }) async {
    FormData formData = FormData.fromMap({
      'file': MultipartFile.fromBytes(
        fileBytes,
        filename: fileName,
      ),
      'name': name,
      if (description != null) 'description': description,
      'document_type': documentType,
      if (courseId != null) 'course_id': courseId,
    });

    final response = await _dio.post('/documents/upload', data: formData);
    return response.data;
  }

  Future<Map<String, dynamic>> processDocument(String documentId) async {
    final response = await _dio.post('/documents/$documentId/process');
    return response.data;
  }

  Future<Map<String, dynamic>> processCurriculum(String documentId, String curriculumName) async {
    FormData formData = FormData.fromMap({
      'curriculum_name': curriculumName,
    });
    final response = await _dio.post('/documents/$documentId/process-curriculum', data: formData);
    return response.data;
  }

  Future<Map<String, dynamic>> processSyllabus(String documentId, String courseId) async {
    FormData formData = FormData.fromMap({
      'course_id': courseId,
    });
    final response = await _dio.post('/documents/$documentId/process-syllabus', data: formData);
    return response.data;
  }

  // Statistics
  Future<Map<String, dynamic>> getQuizStatistics(String quizId) async {
    final response = await _dio.get('/quizzes/$quizId/statistics');
    return response.data;
  }

  Future<Map<String, dynamic>> getQuestionStatistics(String quizId) async {
    final response = await _dio.get('/quizzes/$quizId/question-stats');
    return response.data;
  }

  Future<Map<String, dynamic>> getStudentComparison(String quizId) async {
    final response = await _dio.get('/quizzes/$quizId/student-comparison');
    return response.data;
  }

  Future<Map<String, dynamic>> getCourseStatistics(String courseId) async {
    final response = await _dio.get('/courses/$courseId/statistics');
    return response.data;
  }

  Future<Map<String, dynamic>> getAtRiskStudents(String courseId) async {
    final response = await _dio.get('/analytics/at-risk-students',
        queryParameters: {'course_id': courseId});
    return response.data;
  }

  Future<Map<String, dynamic>> getTeacherDashboard() async {
    final response = await _dio.get('/teacher/dashboard');
    return response.data;
  }

  // Quiz Attempts
  Future<Map<String, dynamic>> startQuiz(String quizId) async {
    final response = await _dio.post('/quizzes/$quizId/start');
    return response.data;
  }

  Future<Map<String, dynamic>> submitQuiz(
      String attemptId, Map<String, String> answers) async {
    final response = await _dio
        .post('/quiz-attempts/$attemptId/submit', data: {'answers': answers});
    return response.data;
  }

  Future<Map<String, dynamic>> getQuizAttempt(String attemptId) async {
    final response = await _dio.get('/quiz-attempts/$attemptId');
    return response.data;
  }

  Future<Map<String, dynamic>> getMyQuizAttempts({String? courseId}) async {
    final response = await _dio.get('/my-quiz-attempts',
        queryParameters: courseId != null ? {'course_id': courseId} : null);
    return response.data;
  }

  // Enrollments
  Future<Map<String, dynamic>> enrollInCourse(String courseId) async {
    final response =
        await _dio.post('/enrollments', data: {'course_id': courseId});
    return response.data;
  }

  Future<Map<String, dynamic>> getMyEnrollments() async {
    final response = await _dio.get('/my-enrollments');
    return response.data;
  }

  Future<Map<String, dynamic>> getCourseEnrollments(String courseId) async {
    final response = await _dio.get('/courses/$courseId/enrollments');
    return response.data;
  }

  Future<void> dropCourse(String enrollmentId) async {
    await _dio.delete('/enrollments/$enrollmentId');
  }

  // Progress
  Future<Map<String, dynamic>> getProgressStats() async {
    final response = await _dio.get('/progress/stats');
    return response.data;
  }

  Future<List<Map<String, dynamic>>> getCourseProgress(String courseId) async {
    final response = await _dio.get('/progress/course/$courseId');
    return List<Map<String, dynamic>>.from(response.data);
  }
}

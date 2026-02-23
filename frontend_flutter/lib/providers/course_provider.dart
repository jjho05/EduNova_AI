import 'package:flutter/material.dart';
import '../models/course.dart';
import '../services/api_service.dart';

class CourseProvider with ChangeNotifier {
  final ApiService _api = ApiService();

  List<Course> _courses = [];
  bool _isLoading = false;
  String? _error;

  List<Course> get courses => _courses;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadCourses() async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _courses = await _api.getCourses();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Course> getCourse(String courseId) async {
    try {
      return await _api.getCourse(courseId);
    } catch (e) {
      throw Exception('Error al cargar curso: $e');
    }
  }

  Future<bool> createCourse(String title, String? description) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      final course = await _api.createCourse(title, description);
      _courses.insert(0, course);

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> deleteCourse(String courseId) async {
    try {
      await _api.deleteCourse(courseId);
      _courses.removeWhere((c) => c.id == courseId);
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }
}

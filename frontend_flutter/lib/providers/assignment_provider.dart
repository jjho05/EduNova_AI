import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../models/assignment.dart';
import '../services/api_service.dart';

class AssignmentProvider with ChangeNotifier {
  final ApiService _api = ApiService();

  List<Assignment> _assignments = [];
  List<Submission> _submissions = [];
  bool _isLoading = false;
  String? _error;

  List<Assignment> get assignments => _assignments;
  List<Submission> get submissions => _submissions;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadCourseAssignments(String courseId) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _assignments = await _api.getCourseAssignments(courseId);

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadMySubmissions() async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _submissions = await _api.getMySubmissions();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> submitAssignment(
      String assignmentId, String? content, PlatformFile? file) async {
    try {
      _isLoading = true;
      notifyListeners();

      await _api.submitAssignment(assignmentId, content, file);
      await loadMySubmissions();

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
}

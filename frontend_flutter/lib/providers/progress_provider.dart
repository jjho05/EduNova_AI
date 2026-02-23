import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ProgressProvider with ChangeNotifier {
  final ApiService _api = ApiService();

  Map<String, dynamic>? _stats;
  bool _isLoading = false;
  String? _error;

  Map<String, dynamic>? get stats => _stats;
  bool get isLoading => _isLoading;
  String? get error => _error;

  double get averageCompletion =>
      _stats?['average_completion']?.toDouble() ?? 0.0;
  int get totalModules => _stats?['total_modules'] ?? 0;
  int get totalTimeMinutes => _stats?['total_time_minutes'] ?? 0;

  Future<void> loadProgressStats() async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _stats = await _api.getProgressStats();

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }
}

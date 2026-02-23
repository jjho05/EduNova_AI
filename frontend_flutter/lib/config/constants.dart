class AppConstants {
  // API - Use relative path for production (works with Hugging Face Spaces)
  // When running locally, change to 'http://localhost:8000/api'
  static const String apiBaseUrl = '/api';

  // Storage Keys
  static const String tokenKey = 'auth_token';
  static const String userKey = 'user_data';

  // Timeouts
  static const Duration connectionTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}

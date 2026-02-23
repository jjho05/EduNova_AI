class User {
  final String id;
  final String email;
  final String name;
  final String role;
  final bool profileComplete;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.name,
    required this.role,
    required this.profileComplete,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      role: json['role'],
      profileComplete: json['profile_complete'] ?? false,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'role': role,
      'profile_complete': profileComplete,
      'created_at': createdAt.toIso8601String(),
    };
  }

  bool get isTeacher => role == 'teacher';
  bool get isStudent => role == 'student';
}

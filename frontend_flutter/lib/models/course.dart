class Course {
  final String id;
  final String userId;
  final String title;
  final String? description;
  final double overallProgress;
  final double? averageGrade;
  final DateTime createdAt;
  final DateTime? updatedAt;

  Course({
    required this.id,
    required this.userId,
    required this.title,
    this.description,
    required this.overallProgress,
    this.averageGrade,
    required this.createdAt,
    this.updatedAt,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['id'],
      userId: json['user_id'],
      title: json['title'],
      description: json['description'],
      overallProgress: (json['overall_progress'] ?? 0.0).toDouble(),
      averageGrade: json['average_grade']?.toDouble(),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'title': title,
      'description': description,
      'overall_progress': overallProgress,
      'average_grade': averageGrade,
      'created_at': createdAt.toIso8601String(),
      if (updatedAt != null) 'updated_at': updatedAt!.toIso8601String(),
    };
  }
}

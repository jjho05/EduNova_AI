class Assignment {
  final String id;
  final String courseId;
  final String? moduleId;
  final String title;
  final String? description;
  final String assignmentType;
  final int maxScore;
  final String? dueDate;
  final String createdAt;

  Assignment({
    required this.id,
    required this.courseId,
    this.moduleId,
    required this.title,
    this.description,
    required this.assignmentType,
    required this.maxScore,
    this.dueDate,
    required this.createdAt,
  });

  factory Assignment.fromJson(Map<String, dynamic> json) {
    return Assignment(
      id: json['id'],
      courseId: json['course_id'],
      moduleId: json['module_id'],
      title: json['title'],
      description: json['description'],
      assignmentType: json['assignment_type'],
      maxScore: json['max_score'],
      dueDate: json['due_date'],
      createdAt: json['created_at'],
    );
  }
}

class Submission {
  final String id;
  final String assignmentId;
  final String studentId;
  final String? content;
  final String? fileUrl;
  final double? score;
  final String? feedback;
  final String submittedAt;
  final String? gradedAt;

  Submission({
    required this.id,
    required this.assignmentId,
    required this.studentId,
    this.content,
    this.fileUrl,
    this.score,
    this.feedback,
    required this.submittedAt,
    this.gradedAt,
  });

  factory Submission.fromJson(Map<String, dynamic> json) {
    return Submission(
      id: json['id'],
      assignmentId: json['assignment_id'],
      studentId: json['student_id'],
      content: json['content'],
      fileUrl: json['file_url'],
      score: json['score']?.toDouble(),
      feedback: json['feedback'],
      submittedAt: json['submitted_at'],
      gradedAt: json['graded_at'],
    );
  }

  bool get isGraded => gradedAt != null;
}

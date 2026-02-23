class Notification {
  final String id;
  final String userId;
  final String title;
  final String message;
  final String notificationType;
  final bool isRead;
  final String? link;
  final String createdAt;

  Notification({
    required this.id,
    required this.userId,
    required this.title,
    required this.message,
    required this.notificationType,
    required this.isRead,
    this.link,
    required this.createdAt,
  });

  factory Notification.fromJson(Map<String, dynamic> json) {
    return Notification(
      id: json['id'],
      userId: json['user_id'],
      title: json['title'],
      message: json['message'],
      notificationType: json['notification_type'],
      isRead: json['is_read'],
      link: json['link'],
      createdAt: json['created_at'],
    );
  }
}

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/assignment_provider.dart';
import '../../config/theme.dart';
import '../../models/assignment.dart';

class AssignmentsListScreen extends StatefulWidget {
  final String courseId;
  
  const AssignmentsListScreen({super.key, required this.courseId});

  @override
  State<AssignmentsListScreen> createState() => _AssignmentsListScreenState();
}

class _AssignmentsListScreenState extends State<AssignmentsListScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AssignmentProvider>().loadCourseAssignments(widget.courseId);
      context.read<AssignmentProvider>().loadMySubmissions();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tareas'),
      ),
      body: Consumer<AssignmentProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading && provider.assignments.isEmpty) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.assignments.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.assignment_outlined, size: 64, color: AppColors.textSecondary),
                  const SizedBox(height: 16),
                  Text(
                    'No hay tareas disponibles',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: provider.assignments.length,
            itemBuilder: (context, index) {
              final assignment = provider.assignments[index];
              final submission = provider.submissions.firstWhere(
                (s) => s.assignmentId == assignment.id,
                orElse: () => Submission(
                  id: '',
                  assignmentId: assignment.id,
                  studentId: '',
                  submittedAt: '',
                ),
              );
              
              return _AssignmentCard(
                assignment: assignment,
                submission: submission.id.isNotEmpty ? submission : null,
              );
            },
          );
        },
      ),
    );
  }
}

class _AssignmentCard extends StatelessWidget {
  final Assignment assignment;
  final Submission? submission;

  const _AssignmentCard({
    required this.assignment,
    this.submission,
  });

  Color _getTypeColor() {
    switch (assignment.assignmentType) {
      case 'exam':
        return AppColors.error;
      case 'project':
        return AppColors.primary;
      case 'quiz':
        return AppColors.warning;
      default:
        return AppColors.success;
    }
  }

  String _getTypeLabel() {
    switch (assignment.assignmentType) {
      case 'exam':
        return 'Examen';
      case 'project':
        return 'Proyecto';
      case 'quiz':
        return 'Quiz';
      default:
        return 'Tarea';
    }
  }

  @override
  Widget build(BuildContext context) {
    final isSubmitted = submission != null;
    final isGraded = submission?.isGraded ?? false;

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: _getTypeColor().withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _getTypeLabel(),
                    style: TextStyle(
                      color: _getTypeColor(),
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
                const Spacer(),
                if (isGraded)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.success.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      '${submission!.score}/${assignment.maxScore}',
                      style: TextStyle(
                        color: AppColors.success,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  )
                else if (isSubmitted)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.warning.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      'Entregado',
                      style: TextStyle(
                        color: AppColors.warning,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              assignment.title,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            if (assignment.description != null) ...[
              const SizedBox(height: 8),
              Text(
                assignment.description!,
                style: TextStyle(color: AppColors.textSecondary),
              ),
            ],
            if (assignment.dueDate != null) ...[
              const SizedBox(height: 12),
              Row(
                children: [
                  Icon(Icons.calendar_today, size: 16, color: AppColors.textSecondary),
                  const SizedBox(width: 8),
                  Text(
                    'Fecha límite: ${assignment.dueDate}',
                    style: TextStyle(
                      color: AppColors.textSecondary,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ],
            if (!isSubmitted) ...[
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    // Navigate to submit screen
                  },
                  child: const Text('Entregar Tarea'),
                ),
              ),
            ],
            if (isGraded && submission!.feedback != null) ...[
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Retroalimentación:',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: AppColors.primary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(submission!.feedback!),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

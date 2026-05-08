import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../config/theme.dart';
import '../../providers/progress_provider.dart';

class ProgressScreen extends StatefulWidget {
  const ProgressScreen({super.key});

  @override
  State<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends State<ProgressScreen> {
  @override
  void initState() {
    super.initState();
    // Load progress data when screen initializes
    Future.microtask(
        () => context.read<ProgressProvider>().loadProgressStats());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mi Progreso'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<ProgressProvider>().loadProgressStats();
            },
            tooltip: 'Actualizar',
          ),
        ],
      ),
      body: Consumer<ProgressProvider>(
        builder: (context, progressProvider, child) {
          if (progressProvider.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (progressProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 64,
                    color: AppColors.error,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Error al cargar progreso',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    progressProvider.error!,
                    style: TextStyle(color: AppColors.textSecondary),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: () {
                      progressProvider.loadProgressStats();
                    },
                    icon: const Icon(Icons.refresh),
                    label: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Summary cards
                Row(
                  children: [
                    Expanded(
                      child: _buildStatCard(
                        'Progreso',
                        '${progressProvider.averageCompletion.toStringAsFixed(1)}%',
                        Icons.trending_up,
                        AppColors.success,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _buildStatCard(
                        'Módulos',
                        '${progressProvider.totalModules}',
                        Icons.book,
                        AppColors.primary,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: _buildStatCard(
                        'Tiempo Total',
                        '${(progressProvider.totalTimeMinutes / 60).toStringAsFixed(1)}h',
                        Icons.access_time,
                        AppColors.secondary,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _buildStatCard(
                        'Promedio Diario',
                        '${(progressProvider.totalTimeMinutes / 30).toStringAsFixed(0)}min',
                        Icons.calendar_today,
                        AppColors.warning,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // Chart Visualization
                if (progressProvider.totalModules > 0) ...[
                  Text(
                    'Visión General',
                    style: Theme.of(context)
                        .textTheme
                        .titleLarge
                        ?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 220,
                    child: Stack(
                      children: [
                        PieChart(
                          PieChartData(
                            sectionsSpace: 0,
                            centerSpaceRadius: 70,
                            sections: [
                              PieChartSectionData(
                                color: _getProgressColor(
                                    progressProvider.averageCompletion),
                                value: progressProvider.averageCompletion > 0
                                    ? progressProvider.averageCompletion
                                    : 1, // Avoid 0 size error
                                title:
                                    '${progressProvider.averageCompletion.toStringAsFixed(1)}%',
                                radius: 30,
                                titleStyle: const TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white),
                              ),
                              PieChartSectionData(
                                color: Colors.grey.withOpacity(0.2),
                                value:
                                    (100 - progressProvider.averageCompletion) >
                                            0
                                        ? (100 -
                                            progressProvider.averageCompletion)
                                        : 0,
                                title: '',
                                radius: 25,
                              ),
                            ],
                          ),
                        ),
                        Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text(
                                'Completado',
                                style:
                                    TextStyle(color: Colors.grey, fontSize: 14),
                              ),
                              Text(
                                '${progressProvider.averageCompletion.toStringAsFixed(0)}%',
                                style: TextStyle(
                                  fontSize: 28,
                                  fontWeight: FontWeight.bold,
                                  color: _getProgressColor(
                                      progressProvider.averageCompletion),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                ],

                // Progress message
                if (progressProvider.stats != null) ...[
                  Card(
                    color: _getProgressColor(progressProvider.averageCompletion)
                        .withOpacity(0.1),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        children: [
                          Icon(
                            _getProgressIcon(
                                progressProvider.averageCompletion),
                            color: _getProgressColor(
                                progressProvider.averageCompletion),
                            size: 32,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  _getProgressMessage(
                                      progressProvider.averageCompletion),
                                  style: Theme.of(context)
                                      .textTheme
                                      .titleMedium
                                      ?.copyWith(
                                        fontWeight: FontWeight.bold,
                                        color: _getProgressColor(
                                            progressProvider.averageCompletion),
                                      ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  _getProgressAdvice(
                                      progressProvider.averageCompletion),
                                  style: TextStyle(
                                    color: AppColors.textSecondary,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],

                // Information message if no data
                if (progressProvider.totalModules == 0) ...[
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          const Icon(
                            Icons.info_outline,
                            size: 64,
                            color: AppColors.primary,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Aún no tienes progreso registrado',
                            style: Theme.of(context).textTheme.titleLarge,
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Inscríbete en un curso y comienza tu aprendizaje para ver tu progreso aquí',
                            style: TextStyle(color: AppColors.textSecondary),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatCard(
      String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                color: AppColors.textSecondary,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getProgressColor(double progress) {
    if (progress >= 80) return AppColors.success;
    if (progress >= 60) return AppColors.warning;
    return AppColors.error;
  }

  IconData _getProgressIcon(double progress) {
    if (progress >= 80) return Icons.emoji_events;
    if (progress >= 60) return Icons.thumb_up;
    return Icons.flag;
  }

  String _getProgressMessage(double progress) {
    if (progress >= 80) return '¡Excelente trabajo!';
    if (progress >= 60) return '¡Buen progreso!';
    if (progress > 0) return '¡Sigue adelante!';
    return 'Comienza tu viaje';
  }

  String _getProgressAdvice(double progress) {
    if (progress >= 80) {
      return 'Estás dominando el material. Sigue con ese ritmo increíble.';
    }
    if (progress >= 60) {
      return 'Vas por buen camino. Un poco más de esfuerzo te llevará lejos.';
    }
    if (progress > 0) {
      return 'Cada paso cuenta. Mantén la constancia y verás resultados.';
    }
    return 'Da el primer paso inscribiéndote en un curso.';
  }
}

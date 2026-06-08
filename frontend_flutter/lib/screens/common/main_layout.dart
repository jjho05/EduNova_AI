import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../providers/auth_provider.dart';

class MainLayout extends StatelessWidget {
  final Widget child;

  const MainLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    // Determine screen width for responsive layout
    final bool isDesktop = MediaQuery.of(context).size.width > 900;
    final String location = GoRouterState.of(context).uri.path;

    return Scaffold(
      body: Row(
        children: [
          if (isDesktop) _buildSidebar(context, location),
          Expanded(
            child: Column(
              children: [
                _buildTopBar(context),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Theme.of(context).scaffoldBackgroundColor,
                    ),
                    child: child,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: !isDesktop ? _buildBottomNav(context, location) : null,
    );
  }

  Widget _buildSidebar(BuildContext context, String location) {
    return Container(
      width: 260,
      decoration: BoxDecoration(
        color: AppColors.darkSurface,
        border: Border(
          right: BorderSide(color: Colors.white.withOpacity(0.05)),
        ),
      ),
      child: Column(
        children: [
          const SizedBox(height: 32),
          // App Logo / Title
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.primary, AppColors.secondary],
                  ),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.auto_awesome, color: Colors.white, size: 24),
              ),
              const SizedBox(width: 12),
              const Text(
                'EduNova AI',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  letterSpacing: 0.5,
                ),
              ),
            ],
          ),
          const SizedBox(height: 48),
          
          // Navigation Items
          _SidebarItem(
            icon: Icons.dashboard_outlined,
            activeIcon: Icons.dashboard,
            label: 'Dashboard',
            isActive: location == '/teacher' || location == '/student',
            onTap: () => context.go(location.startsWith('/teacher') ? '/teacher' : '/student'),
          ),
          _SidebarItem(
            icon: Icons.menu_book_outlined,
            activeIcon: Icons.menu_book,
            label: 'Mis Cursos',
            isActive: location.startsWith('/teacher/courses') || location.startsWith('/course'),
            onTap: () => context.go('/teacher/courses'),
          ),
          _SidebarItem(
            icon: Icons.chat_bubble_outline,
            activeIcon: Icons.chat_bubble,
            label: 'EduChat IA',
            isActive: location == '/chat',
            onTap: () => context.go('/chat'),
          ),
          _SidebarItem(
             icon: Icons.analytics_outlined,
            activeIcon: Icons.analytics,
            label: 'Progreso',
            isActive: location == '/progress',
            onTap: () => context.go('/progress'),
          ),
          _SidebarItem(
            icon: Icons.notifications_none,
            activeIcon: Icons.notifications,
            label: 'Notificaciones',
            isActive: location == '/notifications',
            onTap: () => context.go('/notifications'),
          ),
          
          const Spacer(),
          
          // Bottom profile/logout area
          Padding(
            padding: const EdgeInsets.all(20),
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                   CircleAvatar(
                    backgroundColor: AppColors.primary.withOpacity(0.2),
                    child: const Icon(Icons.person, color: AppColors.primary),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Mi Cuenta', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                        Text('Ver perfil', style: TextStyle(color: Colors.white54, fontSize: 12)),
                      ],
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.logout, color: Colors.white54, size: 18),
                    onPressed: () => context.go('/login'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar(BuildContext context) {
    final dbFallback = context.watch<AuthProvider>().dbFallback;

    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        border: Border(
          bottom: BorderSide(color: Colors.grey.withOpacity(0.1)),
        ),
      ),
      child: Row(
        children: [
          const Text(
            'Panel de Control',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
          ),
          const SizedBox(width: 12),
          Tooltip(
            message: dbFallback
                ? 'Base de datos de respaldo activa (Supabase dormida o inactiva)'
                : 'Conectado a la base de datos principal (Supabase activa)',
            child: Container(
              width: 10,
              height: 10,
              decoration: BoxDecoration(
                color: dbFallback ? AppColors.warning : AppColors.success,
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: (dbFallback ? AppColors.warning : AppColors.success).withOpacity(0.4),
                    blurRadius: 6,
                    spreadRadius: 2,
                  ),
                ],
              ),
            ),
          ),
          const Spacer(),
          Container(
            width: 300,
            height: 40,
            decoration: BoxDecoration(
              color: Colors.grey.withOpacity(0.05),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const TextField(
              decoration: InputDecoration(
                hintText: 'Buscar recursos...',
                prefixIcon: Icon(Icons.search, size: 20),
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                contentPadding: EdgeInsets.only(top: 8),
              ),
            ),
          ),
          const SizedBox(width: 24),
          Stack(
            children: [
              IconButton(onPressed: () {}, icon: const Icon(Icons.notifications_none)),
              Positioned(
                right: 8,
                top: 8,
                child: Container(
                  width: 8,
                  height: 8,
                  decoration: const BoxDecoration(color: Colors.red, shape: BoxShape.circle),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBottomNav(BuildContext context, String location) {
    int currentIndex = 0;
    if (location.startsWith('/teacher') || location.startsWith('/student')) currentIndex = 0;
    else if (location == '/chat') currentIndex = 1;
    else if (location == '/notifications') currentIndex = 2;

    return BottomNavigationBar(
      currentIndex: currentIndex,
      onTap: (index) {
        if (index == 0) context.go('/teacher');
        else if (index == 1) context.go('/chat');
        else if (index == 2) context.go('/notifications');
      },
      items: const [
        BottomNavigationBarItem(icon: Icon(Icons.dashboard_outlined), label: 'Panel'),
        BottomNavigationBarItem(icon: Icon(Icons.chat_bubble_outline), label: 'IA'),
        BottomNavigationBarItem(icon: Icon(Icons.notifications_none), label: 'Avisos'),
      ],
    );
  }
}

class _SidebarItem extends StatelessWidget {
  final IconData icon;
  final IconData activeIcon;
  final String label;
  final bool isActive;
  final VoidCallback onTap;

  const _SidebarItem({
    required this.icon,
    required this.activeIcon,
    required this.label,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: isActive ? AppColors.primary.withOpacity(0.15) : Colors.transparent,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            children: [
              Icon(
                isActive ? activeIcon : icon,
                color: isActive ? AppColors.primary : Colors.white70,
                size: 22,
              ),
              const SizedBox(width: 16),
              Text(
                label,
                style: TextStyle(
                  color: isActive ? Colors.white : Colors.white70,
                  fontWeight: isActive ? FontWeight.w600 : FontWeight.normal,
                  fontSize: 14,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:go_router/go_router.dart';

class ShellScaffold extends StatelessWidget {
  final Widget child;

  const ShellScaffold({Key? key, required this.child}) : super(key: key);

  int _calculateSelectedIndex(BuildContext context) {
    final String location = GoRouterState.of(context).uri.path;
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/explore')) return 1;
    if (location.startsWith('/journal')) return 2;
    if (location.startsWith('/map')) return 3;
    if (location.startsWith('/profile')) return 4;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.go('/home');
        break;
      case 1:
        context.go('/explore');
        break;
      case 2:
        context.go('/journal');
        break;
      case 3:
        context.go('/map');
        break;
      case 4:
        context.go('/profile');
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentIndex = _calculateSelectedIndex(context);

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: child,
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          border: Border(
            top: BorderSide(color: AppColors.divider, width: 1),
          ),
        ),
        child: NavigationBar(
          selectedIndex: currentIndex,
          onDestinationSelected: (index) => _onItemTapped(index, context),
          backgroundColor: AppColors.offWhite,
          indicatorColor: AppColors.caramel.withOpacity(0.2),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.home_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.home_rounded, color: AppColors.caramel),
              label: 'Home',
            ),
            NavigationDestination(
              icon: Icon(Icons.search_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.search_rounded, color: AppColors.caramel),
              label: 'Explore',
            ),
            NavigationDestination(
              icon: Icon(Icons.book_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.book_rounded, color: AppColors.caramel),
              label: 'Journal',
            ),
            NavigationDestination(
              icon: Icon(Icons.map_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.map_rounded, color: AppColors.caramel),
              label: 'Map',
            ),
            NavigationDestination(
              icon: Icon(Icons.person_outline, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.person_rounded, color: AppColors.caramel),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/features/auth/data/auth_repository.dart';
import 'package:brewdrift/core/storage/secure_storage.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _navigate();
  }

  Future<void> _navigate() async {
    // Wait for beautiful splash animation
    await Future.delayed(const Duration(milliseconds: 2800));
    if (!mounted) return;

    final isAuth = await SecureStorage.isAuthenticated();
    if (!mounted) return;

    if (isAuth) {
      context.go(BrewdriftRoutes.home);
    } else {
      final onboardingDone = await SecureStorage.isOnboardingDone();
      if (!mounted) return;
      if (onboardingDone) {
        context.go(BrewdriftRoutes.login);
      } else {
        context.go(BrewdriftRoutes.welcome);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.darkRoast,
      body: Container(
        decoration: const BoxDecoration(gradient: AppColors.splashGradient),
        child: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Coffee icon / logo mark
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.caramel.withOpacity(0.15),
                    border: Border.all(
                      color: AppColors.caramel.withOpacity(0.3),
                      width: 1,
                    ),
                  ),
                  child: const Center(
                    child: Text(
                      '☕',
                      style: TextStyle(fontSize: 36),
                    ),
                  ),
                )
                    .animate()
                    .scale(
                      begin: const Offset(0.5, 0.5),
                      end: const Offset(1.0, 1.0),
                      duration: 800.ms,
                      curve: Curves.elasticOut,
                    )
                    .fadeIn(duration: 600.ms),

                const SizedBox(height: 28),

                // BREWDRIFT wordmark
                const Text(
                  'BREWDRIFT',
                  style: AppTypography.brandLogo,
                )
                    .animate()
                    .fadeIn(delay: 400.ms, duration: 800.ms)
                    .slideY(
                      begin: 0.3,
                      end: 0,
                      delay: 400.ms,
                      duration: 700.ms,
                      curve: Curves.easeOut,
                    ),

                const SizedBox(height: 12),

                // Tagline
                const Text(
                  'Find your vibe. Find your café.',
                  style: AppTypography.brandTagline,
                  textAlign: TextAlign.center,
                )
                    .animate()
                    .fadeIn(delay: 800.ms, duration: 700.ms),

                const SizedBox(height: 80),

                // Loading indicator
                SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(
                      AppColors.caramel.withOpacity(0.6),
                    ),
                  ),
                ).animate().fadeIn(delay: 1400.ms, duration: 400.ms),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

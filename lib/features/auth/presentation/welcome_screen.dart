import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppColors.splashGradient),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.screenPadding,
            ),
            child: Column(
              children: [
                const Spacer(flex: 2),

                // Logo mark
                Container(
                  width: 72,
                  height: 72,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.caramel.withOpacity(0.15),
                    border: Border.all(
                      color: AppColors.caramel.withOpacity(0.4),
                      width: 1.5,
                    ),
                  ),
                  child: const Center(
                    child: Text('☕', style: TextStyle(fontSize: 32)),
                  ),
                )
                    .animate()
                    .scale(
                      begin: const Offset(0.7, 0.7),
                      duration: 600.ms,
                      curve: Curves.easeOut,
                    )
                    .fadeIn(duration: 600.ms),

                const SizedBox(height: 24),

                const Text(
                  'BREWDRIFT',
                  style: AppTypography.brandLogo,
                  textAlign: TextAlign.center,
                ).animate().fadeIn(delay: 200.ms, duration: 600.ms),

                const SizedBox(height: 12),

                const Text(
                  'Your next coffee spot is waiting.',
                  style: AppTypography.brandTagline,
                  textAlign: TextAlign.center,
                ).animate().fadeIn(delay: 400.ms, duration: 600.ms),

                const Spacer(flex: 2),

                // Feature highlights
                _FeatureRow(
                  icon: '🗺️',
                  text: 'Discover cafés around you',
                ).animate().fadeIn(delay: 600.ms, duration: 500.ms),
                const SizedBox(height: 16),
                _FeatureRow(
                  icon: '✨',
                  text: 'Match cafés to your vibe',
                ).animate().fadeIn(delay: 750.ms, duration: 500.ms),
                const SizedBox(height: 16),
                _FeatureRow(
                  icon: '📖',
                  text: 'Keep your café journal',
                ).animate().fadeIn(delay: 900.ms, duration: 500.ms),

                const Spacer(flex: 1),

                // Buttons
                Column(
                  children: [
                    ElevatedButton(
                      onPressed: () => context.go(BrewdriftRoutes.signup),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.caramel,
                        foregroundColor: AppColors.offWhite,
                      ),
                      child: const Text('Create Account'),
                    ),
                    const SizedBox(height: 12),
                    OutlinedButton(
                      onPressed: () => context.go(BrewdriftRoutes.login),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.warmCream,
                        side: const BorderSide(
                          color: AppColors.warmCream,
                          width: 1.5,
                        ),
                      ),
                      child: const Text('Log In'),
                    ),
                  ],
                )
                    .animate()
                    .fadeIn(delay: 1000.ms, duration: 600.ms)
                    .slideY(begin: 0.2, end: 0, delay: 1000.ms, duration: 600.ms),

                const SizedBox(height: 32),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _FeatureRow extends StatelessWidget {
  const _FeatureRow({required this.icon, required this.text});

  final String icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(icon, style: const TextStyle(fontSize: 20)),
        const SizedBox(width: 12),
        Text(
          text,
          style: AppTypography.bodyMedium.copyWith(
            color: AppColors.parchment,
            fontSize: 15,
          ),
        ),
      ],
    );
  }
}

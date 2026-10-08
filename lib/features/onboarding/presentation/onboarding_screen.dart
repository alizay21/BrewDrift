import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/core/storage/secure_storage.dart';
import 'package:brewdrift/core/constants/vibe_definitions.dart';
import 'package:brewdrift/features/auth/data/auth_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/vibe_chip.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final _pageController = PageController();
  int _currentPage = 0;
  final Set<VibeId> _selectedVibes = {};
  bool _isSaving = false;

  final _pages = const [
    _OnboardingPage1(),
    null, // vibes page (built dynamically)
    null, // location page (built dynamically)
    _OnboardingPage4(),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  Future<void> _next() async {
    if (_currentPage < 3) {
      _pageController.nextPage(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    } else {
      await _complete();
    }
  }

  void _skip() {
    _complete();
  }

  Future<void> _complete() async {
    setState(() => _isSaving = true);
    try {
      if (_selectedVibes.isNotEmpty) {
        final vibeIds = _selectedVibes.map((v) => v.name).toList();
        final prefs = const UserPreferences().copyWith(
          preferredVibes: vibeIds,
          onboardingCompleted: true,
        );
        await ref.read(preferencesProvider.notifier).savePreferences(prefs);
      } else {
        await ref.read(preferencesProvider.notifier).setOnboardingComplete();
      }
      await SecureStorage.setOnboardingDone();
      if (mounted) context.go(BrewdriftRoutes.home);
    } catch (_) {
      // Best effort � still let them in
      await SecureStorage.setOnboardingDone();
      if (mounted) context.go(BrewdriftRoutes.home);
    } finally {
      if (mounted) setState(() => _isSaving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: Column(
          children: [
            // Skip + Page indicator
            Padding(
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
                children: [
                  // Page dots
                  Row(
                    children: List.generate(4, (i) => AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      width: _currentPage == i ? 20 : 6,
                      height: 6,
                      margin: const EdgeInsets.only(right: 6),
                      decoration: BoxDecoration(
                        color: _currentPage == i
                            ? AppColors.caramel
                            : AppColors.divider,
                        borderRadius: BorderRadius.circular(AppRadius.full),
                      ),
                    )),
                  ),
                  const Spacer(),
                  TextButton(
                    onPressed: _skip,
                    child: Text(
                      'Skip',
                      style: AppTypography.labelMedium.copyWith(
                        color: AppColors.mochaMedium,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Pages
            Expanded(
              child: PageView(
                controller: _pageController,
                onPageChanged: (p) => setState(() => _currentPage = p),
                children: [
                  const _OnboardingPage1(),
                  _VibesSelectionPage(
                    selectedVibes: _selectedVibes,
                    onVibeToggled: (v) {
                      setState(() {
                        if (_selectedVibes.contains(v)) {
                          _selectedVibes.remove(v);
                        } else {
                          _selectedVibes.add(v);
                        }
                      });
                    },
                  ),
                  const _LocationPage(),
                  const _OnboardingPage4(),
                ],
              ),
            ),

            // Navigation
            Padding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: BrewButton(
                text: _currentPage == 3 ? 'Start Exploring' : 'Continue',
                onPressed: _next,
                isLoading: _isSaving,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _OnboardingPage1 extends StatelessWidget {
  const _OnboardingPage1();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('?', style: TextStyle(fontSize: 80))
              .animate()
              .scale(begin: const Offset(0.7, 0.7), duration: 600.ms, curve: Curves.elasticOut)
              .fadeIn(duration: 400.ms),
          const SizedBox(height: AppSpacing.xl),
          Text(
            'Welcome to\nBrewdrift.',
            style: AppTypography.displayMedium,
            textAlign: TextAlign.center,
          ).animate().fadeIn(delay: 200.ms, duration: 500.ms),
          const SizedBox(height: AppSpacing.md),
          Text(
            'Drift from one beautiful caf� to the next.\nDiscover, experience, and remember.',
            style: AppTypography.caption.copyWith(fontSize: 16),
            textAlign: TextAlign.center,
          ).animate().fadeIn(delay: 400.ms, duration: 500.ms),
          const SizedBox(height: AppSpacing.xl),
          Container(
            padding: const EdgeInsets.all(AppSpacing.md),
            decoration: BoxDecoration(
              color: AppColors.warmCream,
              borderRadius: BorderRadius.circular(AppRadius.md),
            ),
            child: Column(
              children: [
                _FeatureItem(icon: '?', text: 'Find caf�s that match your mood'),
                const SizedBox(height: 12),
                _FeatureItem(icon: '??', text: 'Build your personal caf� journal'),
                const SizedBox(height: 12),
                _FeatureItem(icon: '???', text: 'Map your caf� trail'),
              ],
            ),
          ).animate().fadeIn(delay: 600.ms, duration: 500.ms),
        ],
      ),
    );
  }
}

class _VibesSelectionPage extends StatelessWidget {
  const _VibesSelectionPage({
    required this.selectedVibes,
    required this.onVibeToggled,
  });

  final Set<VibeId> selectedVibes;
  final void Function(VibeId) onVibeToggled;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('? Tell us your vibe.', style: AppTypography.displaySmall),
          const SizedBox(height: AppSpacing.sm),
          Text(
            'Select the vibes that resonate with you.',
            style: AppTypography.bodyMedium,
          ),
          const SizedBox(height: AppSpacing.lg),
          Expanded(
            child: SingleChildScrollView(
              child: Wrap(
                spacing: AppSpacing.chipGap,
                runSpacing: AppSpacing.chipGap,
                children: VibeDefinitions.list.map((vibe) {
                  return VibeChip(
                    vibe: vibe,
                    isSelected: selectedVibes.contains(vibe.id),
                    onTap: () => onVibeToggled(vibe.id),
                  );
                }).toList(),
              ),
            ),
          ),
          if (selectedVibes.isNotEmpty) ...[
            const SizedBox(height: AppSpacing.sm),
            Text(
              '${selectedVibes.length} vibe${selectedVibes.length == 1 ? '' : 's'} selected',
              style: AppTypography.labelSmall.copyWith(color: AppColors.caramel),
            ),
          ],
        ],
      ),
    );
  }
}

class _LocationPage extends StatelessWidget {
  const _LocationPage();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('???', style: TextStyle(fontSize: 80)),
          const SizedBox(height: AppSpacing.xl),
          Text(
            'Find caf�s\naround you.',
            style: AppTypography.displayMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            'Brewdrift uses your location to find real caf�s nearby. We only access it when you\'re searching.',
            style: AppTypography.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.xl),
          Container(
            padding: const EdgeInsets.all(AppSpacing.md),
            decoration: BoxDecoration(
              color: AppColors.warmCream,
              borderRadius: BorderRadius.circular(AppRadius.md),
            ),
            child: Column(
              children: const [
                _FeatureItem(icon: '??', text: 'Used only when discovering caf�s'),
                SizedBox(height: 8),
                _FeatureItem(icon: '??', text: 'Never tracked in the background'),
                SizedBox(height: 8),
                _FeatureItem(icon: '??', text: 'You can change this anytime in Settings'),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          Text(
            'You can also search caf�s manually without location.',
            style: AppTypography.bodySmall.copyWith(
              color: AppColors.mochaMedium.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

class _OnboardingPage4 extends StatelessWidget {
  const _OnboardingPage4();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('??', style: TextStyle(fontSize: 80)),
          const SizedBox(height: AppSpacing.xl),
          Text(
            'Keep your\ncaf� story.',
            style: AppTypography.displayMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.md),
          Text(
            'Every caf� you visit becomes part of your personal journal. Rate, review, and remember.',
            style: AppTypography.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.xl),
          Container(
            padding: const EdgeInsets.all(AppSpacing.md),
            decoration: BoxDecoration(
              color: AppColors.warmCream,
              borderRadius: BorderRadius.circular(AppRadius.md),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '? The Cozy Nook',
                  style: AppTypography.headingSmall,
                ),
                const SizedBox(height: 4),
                const Text('?????', style: TextStyle(fontSize: 18)),
                const SizedBox(height: 6),
                Text(
                  '"Such a peaceful little corner. Loved the natural light."',
                  style: AppTypography.caption,
                ),
                const SizedBox(height: 6),
                Text(
                  'Visited: August 28, 2026',
                  style: AppTypography.labelSmall,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _FeatureItem extends StatelessWidget {
  const _FeatureItem({required this.icon, required this.text});

  final String icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(icon, style: const TextStyle(fontSize: 18)),
        const SizedBox(width: 12),
        Expanded(
          child: Text(text, style: AppTypography.bodyMedium),
        ),
      ],
    );
  }
}

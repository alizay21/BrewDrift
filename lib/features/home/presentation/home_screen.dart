import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/core/utils/location_service.dart';
import 'package:brewdrift/core/utils/date_utils.dart' as brew_dates;
import 'package:brewdrift/features/auth/data/auth_repository.dart';
import 'package:brewdrift/features/home/data/home_repository.dart';
import 'package:brewdrift/shared/widgets/cafe_card.dart';
import 'package:brewdrift/shared/widgets/vibe_chip.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';
import 'package:brewdrift/shared/widgets/error_state.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/core/constants/vibe_definitions.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final _moodController = TextEditingController();

  @override
  void dispose() {
    _moodController.dispose();
    super.dispose();
  }

  Future<void> _findCafes() async {
    final location = ref.read(locationProvider).valueOrNull;
    final selectedVibes = ref.read(selectedVibesProvider);
    final moodText = ref.read(moodTextProvider);

    // Try to fetch location if not available
    if (location == null) {
      await ref.read(locationProvider.notifier).fetchLocation();
    }

    final loc = ref.read(locationProvider).valueOrNull;
    if (loc == null) {
      // No location — redirect to explore for manual search
      if (mounted) context.go(BrewdriftRoutes.explore);
      return;
    }

    await ref.read(recommendationsProvider.notifier).fetch(
      lat: loc.latitude,
      lng: loc.longitude,
      vibes: selectedVibes,
      moodText: moodText,
    );
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(currentUserProvider);
    final selectedVibes = ref.watch(selectedVibesProvider);
    final recommendations = ref.watch(recommendationsProvider);
    final recentVisits = ref.watch(recentVisitsProvider);

    final greeting = brew_dates.greeting();
    final name = user?.displayName.split(' ').first ?? 'there';

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: RefreshIndicator(
        color: AppColors.caramel,
        onRefresh: _findCafes,
        child: CustomScrollView(
          slivers: [
            // ── App Bar ──────────────────────────────────
            SliverAppBar(
              floating: true,
              backgroundColor: AppColors.softBeige,
              elevation: 0,
              expandedHeight: 120,
              flexibleSpace: FlexibleSpaceBar(
                background: Padding(
                  padding: const EdgeInsets.fromLTRB(
                    AppSpacing.screenPadding,
                    0,
                    AppSpacing.screenPadding,
                    0,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Text(
                        '$greeting, $name.',
                        style: AppTypography.headingLarge,
                      ).animate().fadeIn(duration: 500.ms),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        'What are you in the mood for?',
                        style: AppTypography.caption.copyWith(fontSize: 15),
                      ).animate().fadeIn(delay: 100.ms, duration: 500.ms),
                      const SizedBox(height: AppSpacing.sm),
                    ],
                  ),
                ),
              ),
              actions: [
                Padding(
                  padding: const EdgeInsets.only(right: AppSpacing.md),
                  child: GestureDetector(
                    onTap: () => context.go(BrewdriftRoutes.profile),
                    child: CircleAvatar(
                      radius: 18,
                      backgroundColor: AppColors.caramel,
                      child: Text(
                        user?.initials ?? '?',
                        style: const TextStyle(
                          color: AppColors.offWhite,
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),

            SliverPadding(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.screenPadding,
              ),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  const SizedBox(height: AppSpacing.md),

                  // ── Vibe chips ─────────────────────────
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: VibeDefinitions.list.map((vibe) {
                        final isSelected = selectedVibes.contains(vibe.id.name);
                        return Padding(
                          padding: const EdgeInsets.only(right: AppSpacing.chipGap),
                          child: VibeChip(
                            vibe: vibe,
                            isSelected: isSelected,
                            onTap: () {
                              final current = List<String>.from(selectedVibes);
                              if (isSelected) {
                                current.remove(vibe.id.name);
                              } else {
                                current.add(vibe.id.name);
                              }
                              ref.read(selectedVibesProvider.notifier).state = current;
                            },
                          ),
                        );
                      }).toList(),
                    ),
                  ).animate().fadeIn(delay: 200.ms, duration: 400.ms),

                  const SizedBox(height: AppSpacing.md),

                  // ── Mood text ─────────────────────────
                  TextFormField(
                    controller: _moodController,
                    maxLines: 3,
                    minLines: 1,
                    onChanged: (v) => ref.read(moodTextProvider.notifier).state = v,
                    decoration: InputDecoration(
                      hintText: 'Describe your mood... e.g. "somewhere quiet and cute"',
                      hintStyle: AppTypography.bodyMedium,
                      filled: true,
                      fillColor: AppColors.warmCream,
                      contentPadding: const EdgeInsets.all(12),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadius.input),
                        borderSide: BorderSide(color: AppColors.divider),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadius.input),
                        borderSide: BorderSide(color: AppColors.divider),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadius.input),
                        borderSide: BorderSide(color: AppColors.caramel),
                      ),
                    ),
                  ).animate().fadeIn(delay: 300.ms, duration: 400.ms),

                  const SizedBox(height: AppSpacing.md),

                  // ── Find Cafés button ──────────────────
                  ElevatedButton.icon(
                    onPressed: _findCafes,
                    icon: const Text('☕', style: TextStyle(fontSize: 18)),
                    label: Text(
                      selectedVibes.isEmpty ? 'Find Cafés Near Me' : 'Find Cafés for My Vibe',
                      style: AppTypography.buttonText.copyWith(
                        color: AppColors.offWhite,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.espressoBrown,
                      foregroundColor: AppColors.offWhite,
                      minimumSize: const Size(double.infinity, 52),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AppRadius.button),
                      ),
                      elevation: 0,
                    ),
                  ).animate().fadeIn(delay: 350.ms, duration: 400.ms),

                  const SizedBox(height: AppSpacing.sectionGap),

                  // ── Recommendations ────────────────────
                  recommendations.when(
                    data: (recs) {
                      if (recs.isEmpty) return const SizedBox.shrink();
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _SectionHeader(
                            title: selectedVibes.isNotEmpty
                                ? '✨ Your Vibe Matches'
                                : '☕ Near You',
                          ),
                          const SizedBox(height: AppSpacing.md),
                          ListView.separated(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: recs.length.clamp(0, 5),
                            separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.md),
                            itemBuilder: (_, i) {
                              final rec = recs[i];
                              final topVibe = rec.vibeScores.isNotEmpty
                                  ? rec.vibeScores.values.reduce(
                                      (a, b) => a.score > b.score ? a : b,
                                    )
                                  : null;
                              return CafeCard(
                                place: rec.place,
                                vibeMatch: topVibe,
                              );
                            },
                          ),
                          const SizedBox(height: AppSpacing.sectionGap),
                        ],
                      );
                    },
                    loading: () => const BrewLoadingState(),
                    error: (e, __) => BrewErrorState(
                      message: e.toString(),
                      onRetry: _findCafes,
                    ),
                  ),

                  // ── Near You (default) ─────────────────
                  if (recommendations.valueOrNull?.isEmpty ?? true) ...[
                    _SectionHeader(
                      title: '☕ Start Exploring',
                      actionLabel: 'See All',
                      onAction: () => context.go(BrewdriftRoutes.explore),
                    ),
                    const SizedBox(height: AppSpacing.md),
                    BrewEmptyState(
                      icon: '🗺️',
                      title: 'Discover your next café',
                      subtitle: 'Select a mood or tap Find Cafés to get started.',
                      actionLabel: 'Explore Cafés',
                      onAction: () => context.go(BrewdriftRoutes.explore),
                    ),
                    const SizedBox(height: AppSpacing.sectionGap),
                  ],

                  // ── Recent Journal ─────────────────────
                  recentVisits.when(
                    data: (visits) {
                      if (visits.isEmpty) return const SizedBox.shrink();
                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _SectionHeader(
                            title: '📖 Your Café Trail',
                            actionLabel: 'See All',
                            onAction: () => context.go(BrewdriftRoutes.journal),
                          ),
                          const SizedBox(height: AppSpacing.md),
                          ...visits.take(3).map(
                            (v) => Padding(
                              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                              child: _JournalMiniCard(visit: v),
                            ),
                          ),
                          const SizedBox(height: AppSpacing.sectionGap),
                        ],
                      );
                    },
                    loading: () => const SizedBox.shrink(),
                    error: (_, __) => const SizedBox.shrink(),
                  ),

                  const SizedBox(height: 80), // Bottom nav clearance
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title, this.actionLabel, this.onAction});

  final String title;
  final String? actionLabel;
  final VoidCallback? onAction;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Text(title, style: AppTypography.headingSmall),
        ),
        if (actionLabel != null && onAction != null)
          TextButton(
            onPressed: onAction,
            child: Text(
              actionLabel!,
              style: AppTypography.labelMedium.copyWith(color: AppColors.caramel),
            ),
          ),
      ],
    );
  }
}

class _JournalMiniCard extends StatelessWidget {
  const _JournalMiniCard({required this.visit});

  final VisitEntry visit;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.warmCream,
        borderRadius: BorderRadius.circular(AppRadius.md),
      ),
      child: Row(
        children: [
          const Text('☕', style: TextStyle(fontSize: 28)),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  visit.placeNameSnapshot,
                  style: AppTypography.labelLarge,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 2),
                Text(
                  brew_dates.formatVisitDate(visit.visitedAt),
                  style: AppTypography.bodySmall,
                ),
              ],
            ),
          ),
          if (visit.review?.personalRating != null)
            Row(
              children: [
                const Icon(Icons.star_rounded, size: 14, color: AppColors.mutedGold),
                Text(
                  visit.review!.personalRating!.toStringAsFixed(1),
                  style: AppTypography.labelSmall.copyWith(color: AppColors.caramel),
                ),
              ],
            ),
        ],
      ),
    );
  }
}

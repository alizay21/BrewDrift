import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/network/router.dart';
import 'package:brewdrift/core/utils/date_utils.dart' as brew_dates;
import 'package:brewdrift/features/journal/data/journal_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';
import 'package:brewdrift/shared/widgets/error_state.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';

class JournalScreen extends ConsumerWidget {
  const JournalScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final visitsAsync = ref.watch(visitsProvider);

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.softBeige,
        elevation: 0,
        title: const Text('My Café Journal 📖', style: AppTypography.headingMedium),
        centerTitle: false,
      ),
      body: RefreshIndicator(
        color: AppColors.caramel,
        onRefresh: () => ref.read(visitsProvider.notifier).refresh(),
        child: visitsAsync.when(
          data: (visits) {
            if (visits.isEmpty) {
              return const BrewEmptyState(
                icon: '📖',
                title: 'Your journal is empty',
                subtitle: 'Start exploring cafés to save your experiences.\nEvery visit tells a story.',
                actionLabel: 'Explore Cafés',
              );
            }
            return ListView.separated(
              padding: const EdgeInsets.all(AppSpacing.md),
              itemCount: visits.length,
              separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.md),
              itemBuilder: (_, i) => _JournalCard(visit: visits[i]),
            );
          },
          loading: () => const BrewLoadingState(),
          error: (e, _) => BrewErrorState(
            message: e.toString(),
            onRetry: () => ref.read(visitsProvider.notifier).refresh(),
          ),
        ),
      ),
    );
  }
}

class _JournalCard extends StatelessWidget {
  const _JournalCard({required this.visit});

  final VisitEntry visit;

  @override
  Widget build(BuildContext context) {
    final review = visit.review;
    return GestureDetector(
      onTap: () => context.push('/journal/${visit.id}'),
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.offWhite,
          borderRadius: BorderRadius.circular(AppRadius.card),
          boxShadow: AppShadows.card,
        ),
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Photo or emoji
            ClipRRect(
              borderRadius: BorderRadius.circular(AppRadius.sm),
              child: Container(
                width: 72,
                height: 72,
                color: AppColors.warmCream,
                child: review?.photos.isNotEmpty == true
                    ? Image.network(review!.photos.first.storageUrl, fit: BoxFit.cover)
                    : const Center(child: Text('☕', style: TextStyle(fontSize: 32))),
              ),
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(visit.placeNameSnapshot, style: AppTypography.headingSmall, maxLines: 1, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 3),
                  Text(brew_dates.formatVisitDate(visit.visitedAt), style: AppTypography.bodySmall),
                  const SizedBox(height: 6),
                  if (review?.personalRating != null) ...[
                    StarRating(rating: review!.personalRating!, size: 14),
                    const SizedBox(height: 4),
                  ],
                  if (review?.experienceText != null)
                    Text(
                      review!.experienceText!,
                      style: AppTypography.caption,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  if (review?.personalTags.isNotEmpty == true) ...[
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 4,
                      children: review!.personalTags.take(3).map((tag) => Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppColors.caramel.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(AppRadius.full),
                        ),
                        child: Text(tag, style: AppTypography.labelSmall.copyWith(color: AppColors.caramel)),
                      )).toList(),
                    ),
                  ],
                ],
              ),
            ),
            const Icon(Icons.chevron_right_rounded, color: AppColors.mochaMedium),
          ],
        ),
      ),
    );
  }
}

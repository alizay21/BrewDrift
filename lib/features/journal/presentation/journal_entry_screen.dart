import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/utils/date_utils.dart' as brew_dates;
import 'package:brewdrift/features/journal/data/journal_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';
import 'package:brewdrift/shared/widgets/brew_snackbar.dart';

class JournalEntryScreen extends ConsumerWidget {
  const JournalEntryScreen({super.key, required this.visitId});

  final String visitId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Load the visit from the visits list
    final visitsAsync = ref.watch(visitsProvider);

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.softBeige,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new, color: AppColors.espressoBrown, size: 20),
          onPressed: () => context.pop(),
        ),
        title: Text('Journal Entry', style: AppTypography.headingMedium),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit_outlined, color: AppColors.caramel),
            onPressed: () => context.push('/visits/$visitId/edit'),
          ),
        ],
      ),
      body: visitsAsync.when(
        data: (visits) {
          final visit = visits.where((v) => v.id == visitId).firstOrNull;
          if (visit == null) {
            return const Center(child: Text('Entry not found'));
          }
          return _EntryContent(visit: visit);
        },
        loading: () => const InlineLoadingIndicator(),
        error: (e, _) => Center(child: Text(e.toString())),
      ),
    );
  }
}

class _EntryContent extends ConsumerWidget {
  const _EntryContent({required this.visit});

  final VisitEntry visit;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final review = visit.review;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(AppSpacing.md),
            decoration: BoxDecoration(
              gradient: AppColors.warmGradient,
              borderRadius: BorderRadius.circular(AppRadius.card),
            ),
            child: Row(
              children: [
                const Text('☕', style: TextStyle(fontSize: 44)),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(visit.placeNameSnapshot, style: AppTypography.headingSmall),
                      const SizedBox(height: 4),
                      Text(brew_dates.formatVisitDate(visit.visitedAt), style: AppTypography.bodySmall),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.lg),

          // Rating
          if (review?.personalRating != null) ...[
            Text('Your Rating', style: AppTypography.labelLarge),
            const SizedBox(height: 8),
            StarRating(rating: review!.personalRating!, size: 28, showText: true),
            const SizedBox(height: AppSpacing.md),
          ],

          // Experience
          if (review?.experienceText != null && review!.experienceText!.isNotEmpty) ...[
            Text('Your Experience', style: AppTypography.labelLarge),
            const SizedBox(height: 8),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: AppColors.warmCream,
                borderRadius: BorderRadius.circular(AppRadius.md),
              ),
              child: Text('"${review.experienceText!}"', style: AppTypography.caption.copyWith(fontSize: 15)),
            ),
            const SizedBox(height: AppSpacing.md),
          ],

          // Tags
          if (review?.personalTags.isNotEmpty == true) ...[
            Text('Tags', style: AppTypography.labelLarge),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: review!.personalTags.map((tag) => Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: AppColors.caramel.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppRadius.full),
                  border: Border.all(color: AppColors.caramel.withValues(alpha: 0.3)),
                ),
                child: Text('#$tag', style: AppTypography.labelMedium.copyWith(color: AppColors.caramel)),
              )).toList(),
            ),
            const SizedBox(height: AppSpacing.lg),
          ],

          // Photos
          if (review?.photos.isNotEmpty == true) ...[
            Text('Photos', style: AppTypography.labelLarge),
            const SizedBox(height: 8),
            SizedBox(
              height: 120,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                itemCount: review!.photos.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (_, i) => ClipRRect(
                  borderRadius: BorderRadius.circular(AppRadius.sm),
                  child: Image.network(
                    review.photos[i].storageUrl,
                    width: 120,
                    height: 120,
                    fit: BoxFit.cover,
                  ),
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.lg),
          ],

          // Delete button
          OutlinedButton.icon(
            onPressed: () async {
              final confirmed = await showDialog<bool>(
                context: context,
                builder: (_) => AlertDialog(
                  title: const Text('Delete entry?'),
                  content: const Text('This will permanently remove this journal entry.'),
                  actions: [
                    TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
                    TextButton(onPressed: () => Navigator.pop(context, true), child: const Text('Delete', style: TextStyle(color: AppColors.error))),
                  ],
                ),
              );
              if (confirmed == true && context.mounted) {
                await ref.read(visitsProvider.notifier).removeVisit(visit.id);
                if (context.mounted) context.pop();
              }
            },
            icon: const Icon(Icons.delete_outline, color: AppColors.error, size: 18),
            label: const Text('Delete Entry', style: TextStyle(color: AppColors.error)),
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: AppColors.error),
              minimumSize: const Size(double.infinity, 44),
            ),
          ),
        ],
      ),
    );
  }
}

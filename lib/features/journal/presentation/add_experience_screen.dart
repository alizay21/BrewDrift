import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/features/journal/data/journal_repository.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/brew_snackbar.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';

class AddExperienceScreen extends ConsumerStatefulWidget {
  const AddExperienceScreen({
    super.key,
    required this.placeId,
    required this.placeName,
  });

  final String placeId;
  final String placeName;

  @override
  ConsumerState<AddExperienceScreen> createState() => _AddExperienceScreenState();
}

class _AddExperienceScreenState extends ConsumerState<AddExperienceScreen> {
  final _experienceController = TextEditingController();
  double _rating = 0;
  final List<String> _tags = [];
  final _tagController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _experienceController.dispose();
    _tagController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    setState(() => _isLoading = true);
    try {
      // 1. Mark as visited
      final visit = await ref.read(visitsProvider.notifier).addVisit(
        providerPlaceId: widget.placeId,
        placeNameSnapshot: widget.placeName,
        latitude: 0,
        longitude: 0,
        visitedAt: DateTime.now(),
      );

      // 2. Create review if we have content
      if (_rating > 0 || _experienceController.text.isNotEmpty || _tags.isNotEmpty) {
        await ref.read(journalRepositoryProvider).createReview(
          visit.id,
          personalRating: _rating > 0 ? _rating : null,
          experienceText: _experienceController.text.trim().isEmpty ? null : _experienceController.text.trim(),
          personalTags: _tags,
        );
      }

      if (mounted) {
        BrewSnackbar.show(context, '✓ Experience saved to your journal!', isSuccess: true);
        context.pop();
      }
    } catch (e) {
      if (mounted) BrewSnackbar.show(context, e.toString(), isError: true);
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _addTag() {
    final tag = _tagController.text.trim();
    if (tag.isNotEmpty && !_tags.contains(tag) && _tags.length < 8) {
      setState(() {
        _tags.add(tag);
        _tagController.clear();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.softBeige,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new, color: AppColors.espressoBrown, size: 20),
          onPressed: () => context.pop(),
        ),
        title: Text('Add Experience', style: AppTypography.headingMedium),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Place name header
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                gradient: AppColors.warmGradient,
                borderRadius: BorderRadius.circular(AppRadius.card),
              ),
              child: Row(
                children: [
                  const Text('☕', style: TextStyle(fontSize: 36)),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(widget.placeName, style: AppTypography.headingSmall),
                        Text('Visited today', style: AppTypography.bodySmall),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.lg),

            // Rating
            Text('Your Rating', style: AppTypography.labelLarge),
            const SizedBox(height: AppSpacing.sm),
            BrewRatingPicker(
              rating: _rating,
              onRatingChanged: (r) => setState(() => _rating = r),
              size: 40,
            ),
            const SizedBox(height: AppSpacing.lg),

            // Experience
            Text('Your Experience', style: AppTypography.labelLarge),
            const SizedBox(height: AppSpacing.sm),
            TextFormField(
              controller: _experienceController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'How was it? The atmosphere, the coffee, the vibe...',
                hintStyle: AppTypography.bodyMedium,
                filled: true,
                fillColor: AppColors.warmCream,
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
            ),
            const SizedBox(height: AppSpacing.lg),

            // Tags
            Text('Tags (optional)', style: AppTypography.labelLarge),
            const SizedBox(height: AppSpacing.sm),
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _tagController,
                    decoration: InputDecoration(
                      hintText: 'e.g. cozy, good wifi, quiet...',
                      hintStyle: AppTypography.bodySmall,
                      filled: true,
                      fillColor: AppColors.warmCream,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
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
                    onFieldSubmitted: (_) => _addTag(),
                  ),
                ),
                const SizedBox(width: 8),
                GestureDetector(
                  onTap: _addTag,
                  child: Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: AppColors.caramel,
                      borderRadius: BorderRadius.circular(AppRadius.sm),
                    ),
                    child: const Icon(Icons.add, color: AppColors.offWhite),
                  ),
                ),
              ],
            ),
            if (_tags.isNotEmpty) ...[
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 6,
                children: _tags.map((tag) => InputChip(
                  label: Text('#$tag'),
                  deleteIconColor: AppColors.mochaMedium,
                  onDeleted: () => setState(() => _tags.remove(tag)),
                  backgroundColor: AppColors.caramel.withValues(alpha: 0.1),
                  labelStyle: AppTypography.labelMedium.copyWith(color: AppColors.caramel),
                )).toList(),
              ),
            ],
            const SizedBox(height: AppSpacing.xl),

            BrewButton(
              text: 'Save to Journal',
              onPressed: _save,
              isLoading: _isLoading,
            ),
          ],
        ),
      ),
    );
  }
}

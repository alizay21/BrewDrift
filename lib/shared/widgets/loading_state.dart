import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import 'package:brewdrift/core/theme/theme.dart';

/// Base shimmer wrapper
class ShimmerWidget extends StatelessWidget {
  const ShimmerWidget({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Shimmer.fromColors(
      baseColor: AppColors.shimmerBase,
      highlightColor: AppColors.shimmerHighlight,
      child: child,
    );
  }
}

/// Skeleton list for loading state
class BrewLoadingState extends StatelessWidget {
  const BrewLoadingState({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(AppSpacing.md),
      physics: const NeverScrollableScrollPhysics(),
      shrinkWrap: true,
      itemCount: 4,
      separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.md),
      itemBuilder: (_, __) => const CafeCardSkeleton(),
    );
  }
}

/// Skeleton card matching CafeCard dimensions
class CafeCardSkeleton extends StatelessWidget {
  const CafeCardSkeleton({super.key});

  @override
  Widget build(BuildContext context) {
    return ShimmerWidget(
      child: Container(
        height: 220,
        decoration: BoxDecoration(
          color: AppColors.warmCream,
          borderRadius: BorderRadius.circular(AppRadius.card),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 140,
              decoration: BoxDecoration(
                color: AppColors.parchment,
                borderRadius: BorderRadius.vertical(
                  top: Radius.circular(AppRadius.card),
                ),
              ),
            ),
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(width: 150, height: 14, color: AppColors.parchment),
                  const SizedBox(height: 6),
                  Container(width: 100, height: 12, color: AppColors.parchment),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Simple centered spinner
class InlineLoadingIndicator extends StatelessWidget {
  const InlineLoadingIndicator({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Padding(
        padding: EdgeInsets.all(AppSpacing.lg),
        child: CircularProgressIndicator(color: AppColors.caramel, strokeWidth: 2),
      ),
    );
  }
}

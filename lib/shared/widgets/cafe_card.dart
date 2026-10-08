import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';

class CafeCard extends StatelessWidget {
  const CafeCard({
    super.key,
    required this.place,
    this.vibeMatch,
    this.isHorizontal = false,
    this.onTap,
  });

  final Place place;
  final VibeMatch? vibeMatch;
  final bool isHorizontal;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    if (isHorizontal) {
      return _HorizontalCafeCard(place: place, vibeMatch: vibeMatch, onTap: onTap);
    }
    return _VerticalCafeCard(place: place, vibeMatch: vibeMatch, onTap: onTap);
  }
}

class _VerticalCafeCard extends StatelessWidget {
  const _VerticalCafeCard({required this.place, this.vibeMatch, this.onTap});

  final Place place;
  final VibeMatch? vibeMatch;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap ?? () {
        context.push('/places/${place.placeId}', extra: {'place': place.toJson()});
      },
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.offWhite,
          borderRadius: BorderRadius.circular(AppRadius.card),
          boxShadow: AppShadows.card,
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _PlaceImage(place: place, height: 160),
            Padding(
              padding: const EdgeInsets.all(AppSpacing.cardPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          place.name,
                          style: AppTypography.headingSmall,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      if (place.openingHours?.openNow == true)
                        _OpenBadge(isOpen: true)
                      else if (place.openingHours?.openNow == false)
                        _OpenBadge(isOpen: false),
                    ],
                  ),
                  const SizedBox(height: 4),
                  if (place.address != null)
                    Text(
                      place.address!,
                      style: AppTypography.bodySmall,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      if (place.rating != null) ...[
                        StarRating(rating: place.rating!, size: 14),
                        const SizedBox(width: 4),
                        Text(
                          place.rating!.toStringAsFixed(1),
                          style: AppTypography.labelSmall.copyWith(color: AppColors.caramel),
                        ),
                        if (place.ratingCount != null)
                          Text(' (${place.ratingCount})', style: AppTypography.labelSmall),
                        const SizedBox(width: 8),
                      ],
                      if (place.distanceMeters != null)
                        Text(
                          place.displayDistance,
                          style: AppTypography.labelSmall.copyWith(color: AppColors.mochaMedium),
                        ),
                      const Spacer(),
                      if (vibeMatch != null && vibeMatch!.score >= 0.3)
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.caramel.withValues(alpha: 0.12),
                            borderRadius: BorderRadius.circular(AppRadius.xs),
                          ),
                          child: Text(
                            '${vibeMatch!.percentDisplay} match',
                            style: AppTypography.labelSmall.copyWith(
                              color: AppColors.caramel,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HorizontalCafeCard extends StatelessWidget {
  const _HorizontalCafeCard({required this.place, this.vibeMatch, this.onTap});

  final Place place;
  final VibeMatch? vibeMatch;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap ?? () {
        context.push('/places/${place.placeId}', extra: {'place': place.toJson()});
      },
      child: Container(
        width: 200,
        decoration: BoxDecoration(
          color: AppColors.offWhite,
          borderRadius: BorderRadius.circular(AppRadius.card),
          boxShadow: AppShadows.card,
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _PlaceImage(place: place, height: 130),
            Padding(
              padding: const EdgeInsets.all(10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(place.name, style: AppTypography.labelLarge, maxLines: 1, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 3),
                  Row(
                    children: [
                      if (place.rating != null) ...[
                        const Icon(Icons.star_rounded, size: 12, color: AppColors.mutedGold),
                        const SizedBox(width: 2),
                        Text(place.rating!.toStringAsFixed(1), style: AppTypography.labelSmall.copyWith(color: AppColors.caramel)),
                        const SizedBox(width: 6),
                      ],
                      if (place.distanceMeters != null)
                        Text(place.displayDistance, style: AppTypography.labelSmall),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PlaceImage extends StatelessWidget {
  const _PlaceImage({required this.place, required this.height});

  final Place place;
  final double height;

  @override
  Widget build(BuildContext context) {
    final photoUrl = place.photos.isNotEmpty ? place.photos.first.url : null;
    if (photoUrl != null) {
      return CachedNetworkImage(
        imageUrl: photoUrl,
        height: height,
        width: double.infinity,
        fit: BoxFit.cover,
        placeholder: (_, __) => ShimmerWidget(child: Container(height: height, color: AppColors.parchment)),
        errorWidget: (_, __, ___) => _PlaceholderImage(height: height),
      );
    }
    return _PlaceholderImage(height: height);
  }
}

class _PlaceholderImage extends StatelessWidget {
  const _PlaceholderImage({required this.height});

  final double height;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      color: AppColors.parchment,
      child: const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('☕', style: TextStyle(fontSize: 36)),
            SizedBox(height: 4),
            Text('No photo', style: TextStyle(color: AppColors.mochaMedium, fontSize: 11)),
          ],
        ),
      ),
    );
  }
}

class _OpenBadge extends StatelessWidget {
  const _OpenBadge({required this.isOpen});

  final bool isOpen;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: (isOpen ? AppColors.success : AppColors.error).withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(AppRadius.xs),
      ),
      child: Text(
        isOpen ? 'Open' : 'Closed',
        style: AppTypography.labelSmall.copyWith(
          color: isOpen ? AppColors.success : AppColors.error,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}

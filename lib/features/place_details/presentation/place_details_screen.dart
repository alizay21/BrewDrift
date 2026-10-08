import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/features/favorites/data/favorites_repository.dart';
import 'package:brewdrift/features/place_details/data/place_details_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';

class PlaceDetailsScreen extends ConsumerStatefulWidget {
  const PlaceDetailsScreen({
    super.key,
    required this.placeId,
    this.extra,
  });

  final String placeId;
  final Map<String, dynamic>? extra;

  @override
  ConsumerState<PlaceDetailsScreen> createState() => _PlaceDetailsScreenState();
}

class _PlaceDetailsScreenState extends ConsumerState<PlaceDetailsScreen> {
  @override
  Widget build(BuildContext context) {
    final placeAsync = ref.watch(placeDetailsProvider(widget.placeId));
    final favoritesAsync = ref.watch(favoritesProvider);

    // Try to build from extra first (fast path — no network request)
    final preloadedPlace = widget.extra?['place'] is Map<String, dynamic>
        ? Place.fromJson(widget.extra!['place'] as Map<String, dynamic>)
        : null;

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: placeAsync.when(
        data: (place) => _buildContent(place ?? preloadedPlace, favoritesAsync),
        loading: () => preloadedPlace != null
            ? _buildContent(preloadedPlace, favoritesAsync)
            : const Center(child: InlineLoadingIndicator()),
        error: (e, _) => preloadedPlace != null
            ? _buildContent(preloadedPlace, favoritesAsync)
            : Center(child: Text(e.toString())),
      ),
    );
  }

  Widget _buildContent(Place? place, AsyncValue<List<FavoriteEntry>> favAsync) {
    if (place == null) {
      return const Center(child: Text('Café not found'));
    }

    final isFavorited = favAsync.valueOrNull?.any((f) => f.providerPlaceId == place.placeId) ?? false;

    return CustomScrollView(
      slivers: [
        // ── Hero image app bar ───────────────────────────
        SliverAppBar(
          expandedHeight: 300,
          pinned: true,
          backgroundColor: AppColors.offWhite,
          leading: IconButton(
            icon: const CircleAvatar(
              radius: 18,
              backgroundColor: AppColors.espressoBrown,
              child: Icon(Icons.arrow_back_ios_new, color: AppColors.warmCream, size: 16),
            ),
            onPressed: () => context.pop(),
          ),
          actions: [
            IconButton(
              icon: CircleAvatar(
                radius: 18,
                backgroundColor: AppColors.espressoBrown,
                child: Icon(
                  isFavorited ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                  color: isFavorited ? Colors.red : AppColors.warmCream,
                  size: 18,
                ),
              ),
              onPressed: () async {
                if (isFavorited) {
                  final fav = favAsync.valueOrNull?.firstWhere((f) => f.providerPlaceId == place.placeId);
                  if (fav != null) await ref.read(favoritesProvider.notifier).removeFavorite(fav.id);
                } else {
                  await ref.read(favoritesProvider.notifier).addFavorite(
                    provider: 'google',
                    providerPlaceId: place.placeId,
                  );
                }
              },
            ),
          ],
          flexibleSpace: FlexibleSpaceBar(
            background: place.photos.isNotEmpty
                ? CachedNetworkImage(
                    imageUrl: place.photos.first.url ?? '',
                    fit: BoxFit.cover,
                    errorWidget: (_, __, ___) => Container(
                      color: AppColors.parchment,
                      child: const Center(child: Text('☕', style: TextStyle(fontSize: 64))),
                    ),
                  )
                : Container(
                    color: AppColors.parchment,
                    child: const Center(child: Text('☕', style: TextStyle(fontSize: 64))),
                  ),
          ),
        ),

        // ── Main Content ───────────────────────────────────
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Name & Rating
                Text(
                  place.name,
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontFamily: 'PlayfairDisplay',
                        fontWeight: FontWeight.bold,
                        color: AppColors.espressoBrown,
                      ),
                ),
                const SizedBox(height: 8),

                Row(
                  children: [
                    if (place.rating != null) ...[
                      StarRating(rating: place.rating!, size: 18),
                      const SizedBox(width: 6),
                      Text(
                        '${place.rating!.toStringAsFixed(1)} (${place.ratingCount ?? 0})',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(width: 12),
                    ],
                    if (place.isOpenNow)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppColors.sageGreen.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(AppRadius.chip),
                        ),
                        child: const Text(
                          'Open Now',
                          style: TextStyle(color: AppColors.sageGreen, fontSize: 12, fontWeight: FontWeight.w600),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: AppSpacing.md),

                // Address
                if (place.address != null)
                  Row(
                    children: [
                      const Icon(Icons.location_on_outlined, size: 16, color: AppColors.mochaMedium),
                      const SizedBox(width: 4),
                      Expanded(
                        child: Text(
                          place.address!,
                          style: const TextStyle(color: AppColors.mochaMedium, fontSize: 14),
                        ),
                      ),
                    ],
                  ),
                const SizedBox(height: AppSpacing.lg),

                // Actions row
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () => context.push(
                          '/places/${place.placeId}/experience',
                          extra: {'place_name': place.name, 'place': place.toJson()},
                        ),
                        icon: const Text('📖', style: TextStyle(fontSize: 16)),
                        label: const Text('Log Visit'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.espressoBrown,
                          foregroundColor: AppColors.offWhite,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppRadius.button)),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    if (place.phoneNumber != null)
                      IconButton.filled(
                        onPressed: () => launchUrl(Uri.parse('tel:${place.phoneNumber}')),
                        icon: const Icon(Icons.call_outlined),
                        style: IconButton.styleFrom(backgroundColor: AppColors.warmCream, foregroundColor: AppColors.espressoBrown),
                      ),
                    if (place.website != null)
                      IconButton.filled(
                        onPressed: () => launchUrl(Uri.parse(place.website!), mode: LaunchMode.externalApplication),
                        icon: const Icon(Icons.language_outlined),
                        style: IconButton.styleFrom(backgroundColor: AppColors.warmCream, foregroundColor: AppColors.espressoBrown),
                      ),
                  ],
                ),
                const SizedBox(height: AppSpacing.lg),

                // Editorial summary
                if (place.editorialSummary != null) ...[
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    decoration: BoxDecoration(
                      color: AppColors.warmCream,
                      borderRadius: BorderRadius.circular(AppRadius.md),
                    ),
                    child: Text(
                      place.editorialSummary!,
                      style: const TextStyle(
                        fontStyle: FontStyle.italic,
                        color: AppColors.espressoBrown,
                        fontSize: 14,
                      ),
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // Vibe Match breakdown if provided in extra
                if (widget.extra?['vibe_scores'] is Map<String, dynamic>) ...[
                  Text(
                    '✨ Vibe Match',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontFamily: 'PlayfairDisplay',
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 8),
                  ...(widget.extra!['vibe_scores'] as Map<String, dynamic>).entries.map(
                    (entry) => Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Row(
                        children: [
                          Text(entry.key, style: const TextStyle(fontWeight: FontWeight.w600)),
                          const Spacer(),
                          Text('${((entry.value['score'] as num? ?? 0) * 100).round()}%'),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ],
    );
  }
}

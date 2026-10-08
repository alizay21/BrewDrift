import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/core/utils/location_service.dart';
import 'package:brewdrift/features/discovery/data/discovery_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/cafe_card.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';
import 'package:brewdrift/shared/widgets/error_state.dart';

class ExploreScreen extends ConsumerStatefulWidget {
  const ExploreScreen({super.key});

  @override
  ConsumerState<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends ConsumerState<ExploreScreen> {
  bool _isMapView = false;
  bool _openNowFilter = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _loadPlaces());
  }

  Future<void> _loadPlaces() async {
    final loc = ref.read(locationProvider).valueOrNull;
    if (loc == null) {
      await ref.read(locationProvider.notifier).fetchLocation();
    }
    final l = ref.read(locationProvider).valueOrNull;
    if (l != null) {
      await ref.read(nearbyPlacesProvider.notifier).fetch(
        lat: l.latitude,
        lng: l.longitude,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final placesAsync = ref.watch(nearbyPlacesProvider);

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.offWhite,
        elevation: 0,
        titleSpacing: 0,
        title: GestureDetector(
          onTap: () => context.push(BrewdriftRoutes.search),
          child: Container(
            height: 40,
            margin: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
            decoration: BoxDecoration(
              color: AppColors.warmCream,
              borderRadius: BorderRadius.circular(AppRadius.full),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 14),
            child: Row(
              children: [
                const Icon(Icons.search, color: AppColors.mochaMedium, size: 20),
                const SizedBox(width: 8),
                Text('Search for a café...', style: AppTypography.bodyMedium),
              ],
            ),
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(
              _isMapView ? Icons.list_rounded : Icons.map_rounded,
              color: AppColors.espressoBrown,
            ),
            onPressed: () {
              if (_isMapView) {
                setState(() => _isMapView = false);
              } else {
                context.go(BrewdriftRoutes.map);
              }
            },
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(48),
          child: Container(
            color: AppColors.offWhite,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: 8),
              child: Row(
                children: [
                  _FilterChip(
                    label: 'Open Now',
                    selected: _openNowFilter,
                    onSelected: (v) => setState(() => _openNowFilter = v),
                  ),
                  const SizedBox(width: 8),
                  _FilterChip(label: 'Near Me', selected: false, onSelected: (_) {}),
                  const SizedBox(width: 8),
                  _FilterChip(label: '4.0+ Rating', selected: false, onSelected: (_) {}),
                  const SizedBox(width: 8),
                  ActionChip(
                    avatar: const Icon(Icons.tune, size: 16),
                    label: const Text('Filters'),
                    backgroundColor: AppColors.warmCream,
                    onPressed: () => context.push(BrewdriftRoutes.filters),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
      body: RefreshIndicator(
        color: AppColors.caramel,
        onRefresh: _loadPlaces,
        child: placesAsync.when(
          data: (places) {
            if (places.isEmpty) {
              return const BrewEmptyState(
                icon: '☕',
                title: 'No cafés found nearby',
                subtitle: 'Try expanding your search area or search manually.',
              );
            }
            return ListView.separated(
              padding: const EdgeInsets.all(AppSpacing.md),
              itemCount: places.length,
              separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.md),
              itemBuilder: (_, i) => CafeCard(place: places[i]),
            );
          },
          loading: () => const BrewLoadingState(),
          error: (e, _) => BrewErrorState(
            message: e.toString(),
            onRetry: _loadPlaces,
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _loadPlaces,
        backgroundColor: AppColors.caramel,
        child: const Icon(Icons.my_location, color: AppColors.offWhite),
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  const _FilterChip({required this.label, required this.selected, required this.onSelected});

  final String label;
  final bool selected;
  final void Function(bool) onSelected;

  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Text(label, style: AppTypography.labelMedium.copyWith(
        color: selected ? AppColors.offWhite : AppColors.espressoBrown,
      )),
      selected: selected,
      onSelected: onSelected,
      backgroundColor: AppColors.warmCream,
      selectedColor: AppColors.caramel,
      checkmarkColor: AppColors.offWhite,
      side: BorderSide(color: selected ? AppColors.caramel : AppColors.divider),
      showCheckmark: false,
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/core/utils/location_service.dart';
import 'package:brewdrift/features/discovery/data/discovery_repository.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/cafe_card.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';

class MapScreen extends ConsumerStatefulWidget {
  const MapScreen({super.key});

  @override
  ConsumerState<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends ConsumerState<MapScreen> {
  GoogleMapController? _mapController;
  final Set<Marker> _markers = {};
  Place? _selectedPlace;
  bool _isListView = false;

  static const LatLng _defaultCenter = LatLng(37.7749, -122.4194);

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _initialize());
  }

  Future<void> _initialize() async {
    final loc = ref.read(locationProvider).valueOrNull;
    if (loc == null) {
      await ref.read(locationProvider.notifier).fetchLocation();
    }
    _loadNearbyPlaces();
  }

  void _loadNearbyPlaces() {
    final loc = ref.read(locationProvider).valueOrNull;
    if (loc == null) return;
    ref.read(nearbyPlacesProvider.notifier).fetch(
      lat: loc.latitude,
      lng: loc.longitude,
    );
  }

  void _updateMarkers(List<Place> places) {
    setState(() {
      _markers.clear();
      for (final place in places) {
        _markers.add(
          Marker(
            markerId: MarkerId(place.placeId),
            position: LatLng(place.location.lat, place.location.lng),
            infoWindow: InfoWindow(title: place.name),
            icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueOrange),
            onTap: () => setState(() => _selectedPlace = place),
          ),
        );
      }
    });
  }

  void _goToMyLocation() async {
    final loc = ref.read(locationProvider).valueOrNull;
    if (loc == null) {
      await ref.read(locationProvider.notifier).fetchLocation();
      return;
    }
    _mapController?.animateCamera(
      CameraUpdate.newCameraPosition(
        CameraPosition(
          target: LatLng(loc.latitude, loc.longitude),
          zoom: 14.0,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final location = ref.watch(locationProvider).valueOrNull;
    final center = location != null
        ? LatLng(location.latitude, location.longitude)
        : _defaultCenter;

    final placesAsync = ref.watch(nearbyPlacesProvider);

    // Update markers when places load
    ref.listen(nearbyPlacesProvider, (_, next) {
      next.whenData((places) => _updateMarkers(places));
    });

    return Scaffold(
      body: Stack(
        children: [
          // -- Map ----------------------------------------
          GoogleMap(
            onMapCreated: (c) => _mapController = c,
            initialCameraPosition: CameraPosition(target: center, zoom: 14.0),
            myLocationEnabled: location != null,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
            markers: _markers,
            onTap: (_) => setState(() => _selectedPlace = null),
          ),

          // -- Top bar ------------------------------------
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
                children: [
                  // Search pill
                  Expanded(
                    child: GestureDetector(
                      onTap: () => context.push(BrewdriftRoutes.search),
                      child: Container(
                        height: 44,
                        decoration: BoxDecoration(
                          color: AppColors.offWhite,
                          borderRadius: BorderRadius.circular(AppRadius.full),
                          boxShadow: AppShadows.card,
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        child: Row(
                          children: [
                            const Icon(Icons.search, color: AppColors.mochaMedium, size: 20),
                            const SizedBox(width: 8),
                            Text('Search cafés...', style: AppTypography.bodyMedium),
                          ],
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // List/Map toggle
                  GestureDetector(
                    onTap: () => setState(() => _isListView = !_isListView),
                    child: Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        color: AppColors.offWhite,
                        shape: BoxShape.circle,
                        boxShadow: AppShadows.card,
                      ),
                      child: Icon(
                        _isListView ? Icons.map_rounded : Icons.list_rounded,
                        color: AppColors.espressoBrown,
                        size: 22,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // -- Selected place preview ---------------------
          if (_selectedPlace != null)
            Positioned(
              bottom: 90,
              left: AppSpacing.md,
              right: AppSpacing.md,
              child: GestureDetector(
                onTap: () {
                  context.push(
                    '/places/${_selectedPlace!.placeId}',
                    extra: {'place': _selectedPlace!.toJson()},
                  );
                },
                child: Container(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  decoration: BoxDecoration(
                    color: AppColors.offWhite,
                    borderRadius: BorderRadius.circular(AppRadius.card),
                    boxShadow: AppShadows.elevated,
                  ),
                  child: Row(
                    children: [
                      const Text('?', style: TextStyle(fontSize: 28)),
                      const SizedBox(width: AppSpacing.md),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(_selectedPlace!.name, style: AppTypography.headingSmall, maxLines: 1, overflow: TextOverflow.ellipsis),
                            if (_selectedPlace!.address != null)
                              Text(_selectedPlace!.address!, style: AppTypography.bodySmall, maxLines: 1, overflow: TextOverflow.ellipsis),
                            if (_selectedPlace!.rating != null)
                              Row(
                                children: [
                                  const Icon(Icons.star_rounded, size: 14, color: AppColors.mutedGold),
                                  Text(' ${_selectedPlace!.rating!.toStringAsFixed(1)}', style: AppTypography.labelSmall),
                                  if (_selectedPlace!.distanceMeters != null)
                                    Text('  ·  ${_selectedPlace!.displayDistance}', style: AppTypography.labelSmall),
                                ],
                              ),
                          ],
                        ),
                      ),
                      const Icon(Icons.chevron_right_rounded, color: AppColors.mochaMedium),
                    ],
                  ),
                ),
              ),
            ),

          // -- My location FAB ----------------------------
          Positioned(
            bottom: _selectedPlace != null ? 190 : 90,
            right: AppSpacing.md,
            child: FloatingActionButton(
              onPressed: _goToMyLocation,
              backgroundColor: AppColors.offWhite,
              foregroundColor: AppColors.caramel,
              elevation: 2,
              mini: true,
              child: const Icon(Icons.my_location_rounded),
            ),
          ),
        ],
      ),
    );
  }
}

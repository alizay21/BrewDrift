import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/shared/models/models.dart';

class DiscoveryRepository {
  DiscoveryRepository(this._dio);

  final Dio _dio;

  Future<List<Place>> getNearbyPlaces({
    required double lat,
    required double lng,
    int radiusM = 3000,
    int maxResults = 20,
    DiscoveryFilters? filters,
  }) async {
    try {
      final response = await _dio.get('/places/nearby', queryParameters: {
        'lat': lat,
        'lng': lng,
        'radius_m': radiusM,
        'max_results': maxResults,
      });
      final data = response.data as List<dynamic>? ?? [];
      return data.map((e) => Place.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<Place>> searchPlaces({
    required String query,
    double? lat,
    double? lng,
  }) async {
    try {
      final response = await _dio.get('/places/search', queryParameters: {
        'q': query,
        if (lat != null) 'lat': lat,
        if (lng != null) 'lng': lng,
      });
      final data = response.data as List<dynamic>? ?? [];
      return data.map((e) => Place.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<Place?> getPlaceDetails(String placeId) async {
    try {
      final response = await _dio.get('/places/$placeId');
      return Place.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}

// ── Providers ────────────────────────────────────────────

final discoveryRepositoryProvider = Provider<DiscoveryRepository>((ref) {
  return DiscoveryRepository(ApiClient.instance);
});

final discoveryFiltersProvider = StateProvider<DiscoveryFilters>(
  (_) => const DiscoveryFilters(),
);

class NearbyPlacesNotifier extends AsyncNotifier<List<Place>> {
  @override
  Future<List<Place>> build() async => [];

  Future<void> fetch({
    required double lat,
    required double lng,
    DiscoveryFilters? filters,
  }) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(discoveryRepositoryProvider).getNearbyPlaces(
        lat: lat,
        lng: lng,
        filters: filters,
      ),
    );
  }

  void reset() {
    state = const AsyncData([]);
  }
}

final nearbyPlacesProvider =
    AsyncNotifierProvider<NearbyPlacesNotifier, List<Place>>(
      NearbyPlacesNotifier.new,
    );

class SearchPlacesNotifier extends AsyncNotifier<List<Place>> {
  @override
  Future<List<Place>> build() async => [];

  Future<void> search(String query, {double? lat, double? lng}) async {
    if (query.trim().length < 2) {
      state = const AsyncData([]);
      return;
    }
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(discoveryRepositoryProvider).searchPlaces(
        query: query,
        lat: lat,
        lng: lng,
      ),
    );
  }

  void clear() {
    state = const AsyncData([]);
  }
}

final searchPlacesProvider =
    AsyncNotifierProvider<SearchPlacesNotifier, List<Place>>(
      SearchPlacesNotifier.new,
    );

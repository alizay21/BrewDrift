import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/shared/models/models.dart';

class FavoritesRepository {
  FavoritesRepository(this._dio);

  final Dio _dio;

  Future<List<FavoriteEntry>> getFavorites() async {
    try {
      final response = await _dio.get('/favorites');
      final data = response.data as List<dynamic>? ?? [];
      return data.map((e) => FavoriteEntry.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<FavoriteEntry> addFavorite({
    required String provider,
    required String providerPlaceId,
  }) async {
    try {
      final response = await _dio.post('/favorites', data: {
        'provider': provider,
        'provider_place_id': providerPlaceId,
      });
      return FavoriteEntry.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> removeFavorite(String favoriteId) async {
    try {
      await _dio.delete('/favorites/$favoriteId');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}

// ── Providers ────────────────────────────────────────────

final favoritesRepositoryProvider = Provider<FavoritesRepository>(
  (ref) => FavoritesRepository(ApiClient.instance),
);

class FavoritesNotifier extends AsyncNotifier<List<FavoriteEntry>> {
  @override
  Future<List<FavoriteEntry>> build() async {
    return ref.read(favoritesRepositoryProvider).getFavorites();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(favoritesRepositoryProvider).getFavorites(),
    );
  }

  Future<void> addFavorite({
    required String provider,
    required String providerPlaceId,
  }) async {
    final fav = await ref.read(favoritesRepositoryProvider).addFavorite(
      provider: provider,
      providerPlaceId: providerPlaceId,
    );
    state = AsyncData([...state.valueOrNull ?? [], fav]);
  }

  Future<void> removeFavorite(String favoriteId) async {
    await ref.read(favoritesRepositoryProvider).removeFavorite(favoriteId);
    state = AsyncData(
      (state.valueOrNull ?? []).where((f) => f.id != favoriteId).toList(),
    );
  }

  bool isFavorited(String providerPlaceId) {
    return state.valueOrNull?.any((f) => f.providerPlaceId == providerPlaceId) ?? false;
  }
}

final favoritesProvider =
    AsyncNotifierProvider<FavoritesNotifier, List<FavoriteEntry>>(
      FavoritesNotifier.new,
    );

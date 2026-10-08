import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/shared/models/models.dart';

class HomeRepository {
  HomeRepository(this._dio);

  final Dio _dio;

  Future<List<PlaceRecommendation>> getRecommendations({
    required double lat,
    required double lng,
    required List<String> selectedVibes,
    String? moodText,
    int radiusM = 3000,
    double? minRating,
    bool openNow = false,
  }) async {
    try {
      final response = await _dio.post('/recommendations', data: {
        'lat': lat,
        'lng': lng,
        'selected_vibes': selectedVibes,
        if (moodText != null && moodText.isNotEmpty) 'mood_text': moodText,
        'radius_m': radiusM,
        'filters': {
          if (minRating != null) 'min_rating': minRating,
          'open_now': openNow,
        },
      });
      final data = response.data as Map<String, dynamic>;
      final recs = data['recommendations'] as List<dynamic>? ?? [];
      return recs
          .map((e) => PlaceRecommendation.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<List<VisitEntry>> getRecentVisits({int limit = 5}) async {
    try {
      final response = await _dio.get('/visits', queryParameters: {'limit': limit});
      final data = response.data as List<dynamic>? ?? [];
      return data
          .map((e) => VisitEntry.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}

// ── Providers ────────────────────────────────────────────

final homeRepositoryProvider = Provider<HomeRepository>((ref) {
  return HomeRepository(ApiClient.instance);
});

final selectedVibesProvider = StateProvider<List<String>>((ref) => []);
final moodTextProvider = StateProvider<String>((ref) => '');

class RecommendationsNotifier
    extends AsyncNotifier<List<PlaceRecommendation>> {
  @override
  Future<List<PlaceRecommendation>> build() async => [];

  Future<void> fetch({
    required double lat,
    required double lng,
    required List<String> vibes,
    String? moodText,
  }) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(homeRepositoryProvider).getRecommendations(
        lat: lat,
        lng: lng,
        selectedVibes: vibes,
        moodText: moodText,
      ),
    );
  }
}

final recommendationsProvider =
    AsyncNotifierProvider<RecommendationsNotifier, List<PlaceRecommendation>>(
      RecommendationsNotifier.new,
    );

final recentVisitsProvider = FutureProvider<List<VisitEntry>>((ref) {
  return ref.read(homeRepositoryProvider).getRecentVisits();
});

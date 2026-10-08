import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/shared/models/models.dart';

class JournalRepository {
  JournalRepository(this._dio);

  final Dio _dio;

  Future<List<VisitEntry>> getVisits() async {
    try {
      final response = await _dio.get('/visits');
      final data = response.data as List<dynamic>? ?? [];
      return data.map((e) => VisitEntry.fromJson(e as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<VisitEntry> createVisit({
    required String providerPlaceId,
    required String placeNameSnapshot,
    required double latitude,
    required double longitude,
    required DateTime visitedAt,
    String provider = 'google',
  }) async {
    try {
      final response = await _dio.post('/visits', data: {
        'provider': provider,
        'provider_place_id': providerPlaceId,
        'place_name_snapshot': placeNameSnapshot,
        'latitude': latitude,
        'longitude': longitude,
        'visited_at': visitedAt.toIso8601String(),
      });
      return VisitEntry.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<VisitEntry> updateVisit(String visitId, DateTime visitedAt) async {
    try {
      final response = await _dio.patch('/visits/$visitId', data: {
        'visited_at': visitedAt.toIso8601String(),
      });
      return VisitEntry.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deleteVisit(String visitId) async {
    try {
      await _dio.delete('/visits/$visitId');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<PersonalReview?> getReview(String visitId) async {
    try {
      final response = await _dio.get('/visits/$visitId/review');
      return PersonalReview.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      throw mapDioException(e);
    }
  }

  Future<PersonalReview> createReview(
    String visitId, {
    double? personalRating,
    String? experienceText,
    List<String> personalTags = const [],
  }) async {
    try {
      final response = await _dio.post('/visits/$visitId/review', data: {
        if (personalRating != null) 'personal_rating': personalRating,
        if (experienceText != null) 'experience_text': experienceText,
        'personal_tags': personalTags,
      });
      return PersonalReview.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<PersonalReview> updateReview(
    String reviewId, {
    double? personalRating,
    String? experienceText,
    List<String>? personalTags,
  }) async {
    try {
      final response = await _dio.patch('/reviews/$reviewId', data: {
        if (personalRating != null) 'personal_rating': personalRating,
        if (experienceText != null) 'experience_text': experienceText,
        if (personalTags != null) 'personal_tags': personalTags,
      });
      return PersonalReview.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deleteReview(String reviewId) async {
    try {
      await _dio.delete('/reviews/$reviewId');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<ReviewPhoto> uploadPhoto(
    String reviewId, {
    required List<int> bytes,
    required String filename,
    required String mimeType,
  }) async {
    try {
      final formData = FormData.fromMap({
        'file': MultipartFile.fromBytes(bytes, filename: filename, contentType: DioMediaType.parse(mimeType)),
      });
      final response = await _dio.post('/reviews/$reviewId/photos', data: formData);
      return ReviewPhoto.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deletePhoto(String photoId) async {
    try {
      await _dio.delete('/photos/$photoId');
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}

// ── Providers ────────────────────────────────────────────

final journalRepositoryProvider = Provider<JournalRepository>(
  (ref) => JournalRepository(ApiClient.instance),
);

class VisitsNotifier extends AsyncNotifier<List<VisitEntry>> {
  @override
  Future<List<VisitEntry>> build() async {
    return ref.read(journalRepositoryProvider).getVisits();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(journalRepositoryProvider).getVisits(),
    );
  }

  Future<VisitEntry> addVisit({
    required String providerPlaceId,
    required String placeNameSnapshot,
    required double latitude,
    required double longitude,
    required DateTime visitedAt,
  }) async {
    final visit = await ref.read(journalRepositoryProvider).createVisit(
      providerPlaceId: providerPlaceId,
      placeNameSnapshot: placeNameSnapshot,
      latitude: latitude,
      longitude: longitude,
      visitedAt: visitedAt,
    );
    state = AsyncData([visit, ...state.valueOrNull ?? []]);
    return visit;
  }

  Future<void> removeVisit(String visitId) async {
    await ref.read(journalRepositoryProvider).deleteVisit(visitId);
    state = AsyncData(
      (state.valueOrNull ?? []).where((v) => v.id != visitId).toList(),
    );
  }
}

final visitsProvider = AsyncNotifierProvider<VisitsNotifier, List<VisitEntry>>(
  VisitsNotifier.new,
);

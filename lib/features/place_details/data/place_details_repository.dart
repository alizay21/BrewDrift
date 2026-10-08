import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/shared/models/models.dart';

class PlaceDetailsRepository {
  PlaceDetailsRepository(this._dio);

  final Dio _dio;

  Future<Place?> getPlaceDetails(String placeId) async {
    try {
      final response = await _dio.get('/places/$placeId');
      return Place.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      throw mapDioException(e);
    }
  }
}

final placeDetailsRepositoryProvider = Provider<PlaceDetailsRepository>(
  (ref) => PlaceDetailsRepository(ApiClient.instance),
);

final placeDetailsProvider = FutureProvider.family<Place?, String>((ref, placeId) {
  return ref.read(placeDetailsRepositoryProvider).getPlaceDetails(placeId);
});

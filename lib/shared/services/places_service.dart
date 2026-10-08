import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class PlacesService {
  Future<List<Place>> searchNearby(double lat, double lng, double radiusM, dynamic filters) async => [];
  Future<List<Place>> searchByText(String query, [double? lat, double? lng]) async => [];
  Future<Place?> getPlaceDetails(String placeId) async => null;
  Future<List<PlaceRecommendation>> getRecommendations(double lat, double lng, List<String> vibes, String moodText, dynamic filters) async => [];
}

final placesServiceProvider = Provider((ref) => PlacesService());

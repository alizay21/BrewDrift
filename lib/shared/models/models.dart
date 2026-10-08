import 'package:brewdrift/core/constants/vibe_definitions.dart';

/// Internal domain model for a Place (café)
/// Never tied directly to Google's response format
class Place {
  const Place({
    required this.placeId,
    required this.name,
    required this.location,
    this.address,
    this.rating,
    this.ratingCount,
    this.photos = const [],
    this.openingHours,
    this.types = const [],
    this.priceLevel,
    this.phoneNumber,
    this.website,
    this.editorialSummary,
    this.distanceMeters,
  });

  final String placeId;
  final String name;
  final PlaceLocation location;
  final String? address;
  final double? rating;
  final int? ratingCount;
  final List<PlacePhoto> photos;
  final PlaceOpeningHours? openingHours;
  final List<String> types;
  final int? priceLevel;
  final String? phoneNumber;
  final String? website;
  final String? editorialSummary;
  final double? distanceMeters;

  String get displayDistance {
    if (distanceMeters == null) return '';
    if (distanceMeters! < 1000) return '${distanceMeters!.round()} m';
    return '${(distanceMeters! / 1000).toStringAsFixed(1)} km';
  }

  String get priceLevelDisplay {
    if (priceLevel == null) return '';
    return '\$' * priceLevel!;
  }

  bool get isOpenNow => openingHours?.openNow ?? false;

  factory Place.fromJson(Map<String, dynamic> json) {
    return Place(
      placeId: json['place_id'] as String,
      name: json['name'] as String,
      location: PlaceLocation.fromJson(
        json['location'] as Map<String, dynamic>,
      ),
      address: json['address'] as String?,
      rating: (json['rating'] as num?)?.toDouble(),
      ratingCount: json['rating_count'] as int?,
      photos:
          (json['photos'] as List<dynamic>?)
              ?.map(
                (e) => PlacePhoto.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          [],
      openingHours:
          json['opening_hours'] != null
              ? PlaceOpeningHours.fromJson(
                json['opening_hours'] as Map<String, dynamic>,
              )
              : null,
      types: List<String>.from(json['types'] as List<dynamic>? ?? []),
      priceLevel: json['price_level'] as int?,
      phoneNumber: json['phone'] as String?,
      website: json['website'] as String?,
      editorialSummary: json['editorial_summary'] as String?,
      distanceMeters: (json['distance_meters'] as num?)?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() => {
    'place_id': placeId,
    'name': name,
    'location': location.toJson(),
    'address': address,
    'rating': rating,
    'rating_count': ratingCount,
    'photos': photos.map((p) => p.toJson()).toList(),
    'opening_hours': openingHours?.toJson(),
    'types': types,
    'price_level': priceLevel,
    'phone': phoneNumber,
    'website': website,
    'editorial_summary': editorialSummary,
    'distance_meters': distanceMeters,
  };

  Place copyWith({
    String? placeId,
    String? name,
    PlaceLocation? location,
    String? address,
    double? rating,
    int? ratingCount,
    List<PlacePhoto>? photos,
    PlaceOpeningHours? openingHours,
    List<String>? types,
    int? priceLevel,
    String? phoneNumber,
    String? website,
    String? editorialSummary,
    double? distanceMeters,
  }) {
    return Place(
      placeId: placeId ?? this.placeId,
      name: name ?? this.name,
      location: location ?? this.location,
      address: address ?? this.address,
      rating: rating ?? this.rating,
      ratingCount: ratingCount ?? this.ratingCount,
      photos: photos ?? this.photos,
      openingHours: openingHours ?? this.openingHours,
      types: types ?? this.types,
      priceLevel: priceLevel ?? this.priceLevel,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      website: website ?? this.website,
      editorialSummary: editorialSummary ?? this.editorialSummary,
      distanceMeters: distanceMeters ?? this.distanceMeters,
    );
  }
}

class PlaceLocation {
  const PlaceLocation({required this.lat, required this.lng});

  final double lat;
  final double lng;

  factory PlaceLocation.fromJson(Map<String, dynamic> json) {
    return PlaceLocation(
      lat: (json['lat'] as num).toDouble(),
      lng: (json['lng'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => {'lat': lat, 'lng': lng};
}

class PlacePhoto {
  const PlacePhoto({
    required this.photoReference,
    this.url,
    this.width,
    this.height,
    this.attributions = const [],
  });

  final String photoReference;
  final String? url;
  final int? width;
  final int? height;
  final List<String> attributions;

  factory PlacePhoto.fromJson(Map<String, dynamic> json) {
    return PlacePhoto(
      photoReference: json['photo_reference'] as String,
      url: json['url'] as String?,
      width: json['width'] as int?,
      height: json['height'] as int?,
      attributions: List<String>.from(
        json['attributions'] as List<dynamic>? ?? [],
      ),
    );
  }

  Map<String, dynamic> toJson() => {
    'photo_reference': photoReference,
    'url': url,
    'width': width,
    'height': height,
    'attributions': attributions,
  };
}

class PlaceOpeningHours {
  const PlaceOpeningHours({this.openNow, this.weekdayText = const []});

  final bool? openNow;
  final List<String> weekdayText;

  factory PlaceOpeningHours.fromJson(Map<String, dynamic> json) {
    return PlaceOpeningHours(
      openNow: json['open_now'] as bool?,
      weekdayText: List<String>.from(
        json['weekday_text'] as List<dynamic>? ?? [],
      ),
    );
  }

  Map<String, dynamic> toJson() => {
    'open_now': openNow,
    'weekday_text': weekdayText,
  };
}

/// Vibe match result for a Place
class VibeMatch {
  const VibeMatch({
    required this.vibeId,
    required this.score,
    required this.confidence,
    required this.evidence,
  });

  final String vibeId;
  final double score; // 0.0 - 1.0
  final String confidence; // 'high', 'medium', 'low'
  final List<String> evidence;

  String get percentDisplay => '${(score * 100).round()}%';

  bool get isHighConfidence => confidence == 'high';
  bool get isMediumConfidence => confidence == 'medium';

  VibeDefinition? get definition => VibeDefinitions.getById(vibeId);

  String get confidenceLabel {
    switch (confidence) {
      case 'high':
        return 'Strong match';
      case 'medium':
        return 'Good match';
      default:
        return 'Possible match';
    }
  }

  factory VibeMatch.fromJson(Map<String, dynamic> json) {
    return VibeMatch(
      vibeId: json['vibe_id'] as String,
      score: (json['score'] as num).toDouble(),
      confidence: json['confidence'] as String,
      evidence: List<String>.from(json['evidence'] as List<dynamic>? ?? []),
    );
  }

  Map<String, dynamic> toJson() => {
    'vibe_id': vibeId,
    'score': score,
    'confidence': confidence,
    'evidence': evidence,
  };
}

/// Full recommendation result from the backend
class PlaceRecommendation {
  const PlaceRecommendation({
    required this.place,
    required this.vibeScores,
    required this.overallScore,
    required this.confidence,
    required this.evidence,
  });

  final Place place;
  final Map<String, VibeMatch> vibeScores;
  final double overallScore;
  final String confidence;
  final List<String> evidence;

  String get matchPercentDisplay => '${(overallScore * 100).round()}%';

  factory PlaceRecommendation.fromJson(Map<String, dynamic> json) {
    final scoresMap = json['vibe_scores'] as Map<String, dynamic>? ?? {};
    return PlaceRecommendation(
      place: Place.fromJson(json['place'] as Map<String, dynamic>),
      vibeScores: scoresMap.map(
        (k, v) => MapEntry(k, VibeMatch.fromJson(v as Map<String, dynamic>)),
      ),
      overallScore: (json['overall_score'] as num).toDouble(),
      confidence: json['confidence'] as String,
      evidence: List<String>.from(json['evidence'] as List<dynamic>? ?? []),
    );
  }
}

/// User's visited place entry
class VisitEntry {
  const VisitEntry({
    required this.id,
    required this.provider,
    required this.providerPlaceId,
    required this.placeNameSnapshot,
    required this.latitude,
    required this.longitude,
    required this.visitedAt,
    required this.createdAt,
    this.review,
  });

  final String id;
  final String provider;
  final String providerPlaceId;
  final String placeNameSnapshot;
  final double latitude;
  final double longitude;
  final DateTime visitedAt;
  final DateTime createdAt;
  final PersonalReview? review;

  factory VisitEntry.fromJson(Map<String, dynamic> json) {
    return VisitEntry(
      id: json['id'] as String,
      provider: json['provider'] as String,
      providerPlaceId: json['provider_place_id'] as String,
      placeNameSnapshot: json['place_name_snapshot'] as String,
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      visitedAt: DateTime.parse(json['visited_at'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
      review:
          json['review'] != null
              ? PersonalReview.fromJson(json['review'] as Map<String, dynamic>)
              : null,
    );
  }
}

/// User's personal review for a visited place
class PersonalReview {
  const PersonalReview({
    required this.id,
    required this.visitedPlaceId,
    this.personalRating,
    this.experienceText,
    this.personalTags = const [],
    this.photos = const [],
    required this.createdAt,
    required this.updatedAt,
  });

  final String id;
  final String visitedPlaceId;
  final double? personalRating;
  final String? experienceText;
  final List<String> personalTags;
  final List<ReviewPhoto> photos;
  final DateTime createdAt;
  final DateTime updatedAt;

  factory PersonalReview.fromJson(Map<String, dynamic> json) {
    return PersonalReview(
      id: json['id'] as String,
      visitedPlaceId: json['visited_place_id'] as String,
      personalRating: (json['personal_rating'] as num?)?.toDouble(),
      experienceText: json['experience_text'] as String?,
      personalTags: List<String>.from(
        json['personal_tags'] as List<dynamic>? ?? [],
      ),
      photos:
          (json['photos'] as List<dynamic>?)
              ?.map(
                (e) => ReviewPhoto.fromJson(e as Map<String, dynamic>),
              )
              .toList() ??
          [],
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}

class ReviewPhoto {
  const ReviewPhoto({
    required this.id,
    required this.reviewId,
    required this.storageUrl,
    required this.filename,
    required this.createdAt,
  });

  final String id;
  final String reviewId;
  final String storageUrl;
  final String filename;
  final DateTime createdAt;

  factory ReviewPhoto.fromJson(Map<String, dynamic> json) {
    return ReviewPhoto(
      id: json['id'] as String,
      reviewId: json['review_id'] as String,
      storageUrl: json['storage_url'] as String,
      filename: json['filename'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

/// User's favorite entry
class FavoriteEntry {
  const FavoriteEntry({
    required this.id,
    required this.provider,
    required this.providerPlaceId,
    required this.createdAt,
  });

  final String id;
  final String provider;
  final String providerPlaceId;
  final DateTime createdAt;

  factory FavoriteEntry.fromJson(Map<String, dynamic> json) {
    return FavoriteEntry(
      id: json['id'] as String,
      provider: json['provider'] as String,
      providerPlaceId: json['provider_place_id'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

/// User's collection
class CafeCollection {
  const CafeCollection({
    required this.id,
    required this.name,
    this.description,
    this.coverPhotoUrl,
    required this.itemCount,
    required this.createdAt,
  });

  final String id;
  final String name;
  final String? description;
  final String? coverPhotoUrl;
  final int itemCount;
  final DateTime createdAt;

  factory CafeCollection.fromJson(Map<String, dynamic> json) {
    return CafeCollection(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String?,
      coverPhotoUrl: json['cover_photo_url'] as String?,
      itemCount: json['item_count'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

/// Brewdrift user profile
class BrewdriftUser {
  const BrewdriftUser({
    required this.id,
    required this.email,
    required this.displayName,
    required this.username,
    this.bio,
    this.profilePhotoUrl,
    required this.createdAt,
  });

  final String id;
  final String email;
  final String displayName;
  final String username;
  final String? bio;
  final String? profilePhotoUrl;
  final DateTime createdAt;

  String get initials {
    final parts = displayName.trim().split(' ');
    if (parts.length >= 2) {
      return '${parts.first[0]}${parts.last[0]}'.toUpperCase();
    }
    return displayName.substring(0, displayName.length.clamp(0, 2)).toUpperCase();
  }

  factory BrewdriftUser.fromJson(Map<String, dynamic> json) {
    return BrewdriftUser(
      id: json['id'] as String,
      email: json['email'] as String,
      displayName: json['display_name'] as String,
      username: json['username'] as String,
      bio: json['bio'] as String?,
      profilePhotoUrl: json['profile_photo_url'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'display_name': displayName,
    'username': username,
    'bio': bio,
    'profile_photo_url': profilePhotoUrl,
    'created_at': createdAt.toIso8601String(),
  };
}

/// User preferences
class UserPreferences {
  const UserPreferences({
    this.preferredVibes = const [],
    this.preferredMaxDistanceKm = 5,
    this.preferredMinRating = 0.0,
    this.onboardingCompleted = false,
  });

  final List<String> preferredVibes;
  final int preferredMaxDistanceKm;
  final double preferredMinRating;
  final bool onboardingCompleted;

  factory UserPreferences.fromJson(Map<String, dynamic> json) {
    return UserPreferences(
      preferredVibes: List<String>.from(
        json['preferred_vibes'] as List<dynamic>? ?? [],
      ),
      preferredMaxDistanceKm: json['preferred_max_distance_km'] as int? ?? 5,
      preferredMinRating:
          (json['preferred_min_rating'] as num?)?.toDouble() ?? 0.0,
      onboardingCompleted: json['onboarding_completed'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
    'preferred_vibes': preferredVibes,
    'preferred_max_distance_km': preferredMaxDistanceKm,
    'preferred_min_rating': preferredMinRating,
    'onboarding_completed': onboardingCompleted,
  };

  UserPreferences copyWith({
    List<String>? preferredVibes,
    int? preferredMaxDistanceKm,
    double? preferredMinRating,
    bool? onboardingCompleted,
  }) {
    return UserPreferences(
      preferredVibes: preferredVibes ?? this.preferredVibes,
      preferredMaxDistanceKm:
          preferredMaxDistanceKm ?? this.preferredMaxDistanceKm,
      preferredMinRating: preferredMinRating ?? this.preferredMinRating,
      onboardingCompleted: onboardingCompleted ?? this.onboardingCompleted,
    );
  }
}

/// Filter options for café discovery
class DiscoveryFilters {
  const DiscoveryFilters({
    this.maxDistanceKm = 5,
    this.minRating = 0.0,
    this.selectedVibes = const [],
    this.openNow = false,
    this.sortBy = SortBy.bestMatch,
  });

  final int maxDistanceKm;
  final double minRating;
  final List<String> selectedVibes;
  final bool openNow;
  final SortBy sortBy;

  DiscoveryFilters copyWith({
    int? maxDistanceKm,
    double? minRating,
    List<String>? selectedVibes,
    bool? openNow,
    SortBy? sortBy,
  }) {
    return DiscoveryFilters(
      maxDistanceKm: maxDistanceKm ?? this.maxDistanceKm,
      minRating: minRating ?? this.minRating,
      selectedVibes: selectedVibes ?? this.selectedVibes,
      openNow: openNow ?? this.openNow,
      sortBy: sortBy ?? this.sortBy,
    );
  }
}

enum SortBy { bestMatch, distance, rating }

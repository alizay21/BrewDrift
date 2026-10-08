/// Brewdrift app-wide constants
class AppConstants {
  AppConstants._();

  static const String appName = 'Brewdrift';
  static const String tagline = 'Find your vibe. Find your café.';
  static const String taglineAlt = 'Your next coffee spot is waiting.';

  // API
  static const int connectTimeoutMs = 15000;
  static const int receiveTimeoutMs = 30000;
  static const int maxRetries = 2;
  static const int searchDebounceMs = 400;

  // Auth
  static const String accessTokenKey = 'brewdrift_access_token';
  static const String refreshTokenKey = 'brewdrift_refresh_token';
  static const String userIdKey = 'brewdrift_user_id';
  static const String onboardingDoneKey = 'brewdrift_onboarding_done';

  // Places
  static const int defaultRadiusMeters = 3000;
  static const int maxSearchResults = 20;
  static const double defaultMinRating = 0.0;
  static const String defaultPlaceProvider = 'google';

  // Images
  static const int maxPhotosPerReview = 5;
  static const int maxUploadSizeMb = 10;
  static const int imageMaxDimension = 1500;
  static const int imageJpegQuality = 80;

  // Pagination
  static const int pageSize = 15;

  // Map
  static const double defaultMapZoom = 14.5;
  static const double detailsMapZoom = 15.5;

  // Cache
  static const int recentSearchesCacheCount = 8;

  // Onboarding
  static const int onboardingPageCount = 4;
}

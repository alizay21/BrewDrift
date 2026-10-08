import 'package:geolocator/geolocator.dart' hide LocationServiceDisabledException;
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../errors/app_exception.dart';

class LocationService {
  /// Get current location, handling all permission states
  Future<Position> getCurrentLocation() async {
    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw const LocationServiceDisabledException();
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw const LocationPermissionDeniedException();
      }
    }

    if (permission == LocationPermission.deniedForever) {
      throw const LocationPermissionDeniedException(
        'Location is permanently denied. Enable it in Settings.',
      );
    }

    try {
      return await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.medium,
          timeLimit: Duration(seconds: 10),
        ),
      );
    } catch (e) {
      throw LocationException('Could not get location: $e');
    }
  }

  Future<LocationPermissionStatus> getPermissionStatus() async {
    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return LocationPermissionStatus.serviceDisabled;

    final permission = await Geolocator.checkPermission();
    switch (permission) {
      case LocationPermission.always:
      case LocationPermission.whileInUse:
        return LocationPermissionStatus.granted;
      case LocationPermission.denied:
        return LocationPermissionStatus.denied;
      case LocationPermission.deniedForever:
        return LocationPermissionStatus.permanentlyDenied;
      default:
        return LocationPermissionStatus.denied;
    }
  }

  Future<void> openSettings() async => Geolocator.openAppSettings();
  Future<void> openLocationSettings() async => Geolocator.openLocationSettings();

  double distanceBetween({
    required double lat1,
    required double lng1,
    required double lat2,
    required double lng2,
  }) {
    return Geolocator.distanceBetween(lat1, lng1, lat2, lng2);
  }
}

enum LocationPermissionStatus {
  granted,
  denied,
  permanentlyDenied,
  serviceDisabled,
}

// ── Riverpod Providers ────────────────────────────────────

final locationServiceProvider = Provider<LocationService>(
  (_) => LocationService(),
);

class LocationNotifier extends AsyncNotifier<Position?> {
  @override
  Future<Position?> build() async => null;

  Future<void> fetchLocation() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(locationServiceProvider).getCurrentLocation(),
    );
  }

  void clearLocation() {
    state = const AsyncData(null);
  }
}

final locationProvider = AsyncNotifierProvider<LocationNotifier, Position?>(
  LocationNotifier.new,
);

final locationPermissionProvider = FutureProvider<LocationPermissionStatus>(
  (ref) => ref.read(locationServiceProvider).getPermissionStatus(),
);

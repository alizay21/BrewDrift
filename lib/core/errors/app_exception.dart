/// Brewdrift application exceptions
abstract class AppException implements Exception {
  const AppException(this.message, {this.code});

  final String message;
  final String? code;

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  const NetworkException([super.message = 'Connection failed. Check your internet.']);
}

class TimeoutException extends AppException {
  const TimeoutException([super.message = 'Request timed out. Please try again.']);
}

class ServerException extends AppException {
  const ServerException([super.message = 'Server error. Please try again later.']);
}

class UnauthorizedException extends AppException {
  const UnauthorizedException([super.message = 'Session expired. Please log in again.']);
}

class ForbiddenException extends AppException {
  const ForbiddenException([super.message = 'You do not have permission to do this.']);
}

class NotFoundException extends AppException {
  const NotFoundException([super.message = 'Not found.']);
}

class ValidationException extends AppException {
  const ValidationException(super.message);
}

class ConflictException extends AppException {
  const ConflictException(super.message);
}

class LocationException extends AppException {
  const LocationException([super.message = 'Unable to get your location.']);
}

class LocationPermissionDeniedException extends AppException {
  const LocationPermissionDeniedException([
    super.message = 'Location permission denied.',
  ]);
}

class LocationServiceDisabledException extends AppException {
  const LocationServiceDisabledException([
    super.message = 'Location services are disabled.',
  ]);
}

class UploadException extends AppException {
  const UploadException([super.message = 'Upload failed. Please try again.']);
}

class CacheException extends AppException {
  const CacheException([super.message = 'Cache error.']);
}

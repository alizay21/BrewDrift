import 'package:dio/dio.dart';
import '../errors/app_exception.dart' as brew_exceptions;

/// Maps DioExceptions and HTTP status codes to AppExceptions
brew_exceptions.AppException mapDioException(DioException e) {
  if (e.type == DioExceptionType.connectionTimeout ||
      e.type == DioExceptionType.receiveTimeout ||
      e.type == DioExceptionType.sendTimeout) {
    return const brew_exceptions.TimeoutException();
  }

  if (e.type == DioExceptionType.connectionError) {
    return const brew_exceptions.NetworkException();
  }

  final statusCode = e.response?.statusCode;
  final data = e.response?.data;
  String? serverMessage;
  if (data is Map<String, dynamic>) {
    serverMessage =
        data['detail'] as String? ??
        data['message'] as String? ??
        data['error'] as String?;
  }

  switch (statusCode) {
    case 400:
      return brew_exceptions.ValidationException(
        serverMessage ?? 'Invalid request.',
      );
    case 401:
      return const brew_exceptions.UnauthorizedException();
    case 403:
      return const brew_exceptions.ForbiddenException();
    case 404:
      return const brew_exceptions.NotFoundException();
    case 409:
      return brew_exceptions.ConflictException(
        serverMessage ?? 'Conflict. This already exists.',
      );
    case 422:
      return brew_exceptions.ValidationException(
        serverMessage ?? 'Validation failed.',
      );
    case null:
      return const brew_exceptions.NetworkException();
    default:
      if (statusCode != null && statusCode >= 500) {
        return const brew_exceptions.ServerException();
      }
      return brew_exceptions.ServerException(
        serverMessage ?? 'Something went wrong.',
      );
  }
}

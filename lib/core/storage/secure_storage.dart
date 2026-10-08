import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';

/// Secure storage wrapper using Android Keystore
class SecureStorage {
  SecureStorage._();

  static const FlutterSecureStorage _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
  );

  // ── Tokens ───────────────────────────────────────────────
  static Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await Future.wait([
      _storage.write(
        key: AppConstants.accessTokenKey,
        value: accessToken,
      ),
      _storage.write(
        key: AppConstants.refreshTokenKey,
        value: refreshToken,
      ),
    ]);
  }

  static Future<String?> getAccessToken() async {
    return _storage.read(key: AppConstants.accessTokenKey);
  }

  static Future<String?> getRefreshToken() async {
    return _storage.read(key: AppConstants.refreshTokenKey);
  }

  // ── User ─────────────────────────────────────────────────
  static Future<void> saveUserId(String userId) async {
    await _storage.write(key: AppConstants.userIdKey, value: userId);
  }

  static Future<String?> getUserId() async {
    return _storage.read(key: AppConstants.userIdKey);
  }

  // ── Onboarding ───────────────────────────────────────────
  static Future<void> setOnboardingDone() async {
    await _storage.write(key: AppConstants.onboardingDoneKey, value: 'true');
  }

  static Future<bool> isOnboardingDone() async {
    final value = await _storage.read(key: AppConstants.onboardingDoneKey);
    return value == 'true';
  }

  // ── Auth State ───────────────────────────────────────────
  static Future<bool> isAuthenticated() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  // ── Clear ────────────────────────────────────────────────
  static Future<void> clearAll() async {
    await _storage.deleteAll();
  }

  static Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: AppConstants.accessTokenKey),
      _storage.delete(key: AppConstants.refreshTokenKey),
    ]);
  }
}

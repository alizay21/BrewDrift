import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/core/network/api_client.dart';
import 'package:brewdrift/core/storage/secure_storage.dart';
import 'package:brewdrift/core/errors/failure.dart';
import 'package:brewdrift/core/errors/app_exception.dart';
import 'package:brewdrift/shared/models/models.dart';

class AuthRepository {
  AuthRepository(this._dio);

  final Dio _dio;

  Future<BrewdriftUser> register({
    required String email,
    required String password,
    required String displayName,
    required String username,
  }) async {
    try {
      final response = await _dio.post('/auth/register', data: {
        'email': email,
        'password': password,
        'display_name': displayName,
        'username': username,
      });
      final data = response.data as Map<String, dynamic>;
      await SecureStorage.saveTokens(
        accessToken: data['access_token'] as String,
        refreshToken: data['refresh_token'] as String,
      );
      final user = BrewdriftUser.fromJson(
        data['user'] as Map<String, dynamic>,
      );
      await SecureStorage.saveUserId(user.id);
      return user;
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<BrewdriftUser> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _dio.post('/auth/login', data: {
        'email': email,
        'password': password,
      });
      final data = response.data as Map<String, dynamic>;
      await SecureStorage.saveTokens(
        accessToken: data['access_token'] as String,
        refreshToken: data['refresh_token'] as String,
      );
      // Fetch user profile
      final userResp = await _dio.get('/users/me');
      final user = BrewdriftUser.fromJson(
        userResp.data as Map<String, dynamic>,
      );
      await SecureStorage.saveUserId(user.id);
      return user;
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> logout() async {
    try {
      await _dio.post('/auth/logout');
    } catch (_) {
      // Best effort; clear local tokens regardless
    }
    await SecureStorage.clearAll();
  }

  Future<BrewdriftUser> getCurrentUser() async {
    try {
      final response = await _dio.get('/users/me');
      return BrewdriftUser.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> forgotPassword(String email) async {
    try {
      await _dio.post('/auth/forgot-password', data: {'email': email});
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> resetPassword({
    required String token,
    required String newPassword,
  }) async {
    try {
      await _dio.post('/auth/reset-password', data: {
        'token': token,
        'new_password': newPassword,
      });
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<BrewdriftUser> updateProfile({
    String? displayName,
    String? username,
    String? bio,
  }) async {
    try {
      final response = await _dio.patch('/users/me', data: {
        if (displayName != null) 'display_name': displayName,
        if (username != null) 'username': username,
        if (bio != null) 'bio': bio,
      });
      return BrewdriftUser.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<void> deleteAccount() async {
    try {
      await _dio.delete('/users/me');
      await SecureStorage.clearAll();
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<UserPreferences> getPreferences() async {
    try {
      final response = await _dio.get('/users/me/preferences');
      return UserPreferences.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }

  Future<UserPreferences> updatePreferences(UserPreferences prefs) async {
    try {
      final response = await _dio.put(
        '/users/me/preferences',
        data: prefs.toJson(),
      );
      return UserPreferences.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      throw mapDioException(e);
    }
  }
}

// ── Riverpod Providers ────────────────────────────────────

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(ApiClient.instance);
});

/// Auth state — manages current user session
class AuthNotifier extends AsyncNotifier<BrewdriftUser?> {
  @override
  Future<BrewdriftUser?> build() async {
    final isAuth = await SecureStorage.isAuthenticated();
    if (!isAuth) return null;
    try {
      return await ref.read(authRepositoryProvider).getCurrentUser();
    } catch (_) {
      await SecureStorage.clearAll();
      return null;
    }
  }

  Future<void> login({required String email, required String password}) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(authRepositoryProvider).login(
        email: email,
        password: password,
      ),
    );
  }

  Future<void> register({
    required String email,
    required String password,
    required String displayName,
    required String username,
  }) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(
      () => ref.read(authRepositoryProvider).register(
        email: email,
        password: password,
        displayName: displayName,
        username: username,
      ),
    );
  }

  Future<void> logout() async {
    await ref.read(authRepositoryProvider).logout();
    state = const AsyncData(null);
  }

  Future<void> updateProfile({
    String? displayName,
    String? username,
    String? bio,
  }) async {
    final user = await ref.read(authRepositoryProvider).updateProfile(
      displayName: displayName,
      username: username,
      bio: bio,
    );
    state = AsyncData(user);
  }

  Future<void> deleteAccount() async {
    await ref.read(authRepositoryProvider).deleteAccount();
    state = const AsyncData(null);
  }
}

final authProvider = AsyncNotifierProvider<AuthNotifier, BrewdriftUser?>(
  AuthNotifier.new,
);

/// Convenience: is user authenticated?
final isAuthenticatedProvider = Provider<bool>((ref) {
  return ref.watch(authProvider).valueOrNull != null;
});

/// Convenience: current user (non-null when authenticated)
final currentUserProvider = Provider<BrewdriftUser?>((ref) {
  return ref.watch(authProvider).valueOrNull;
});

/// User preferences
class PreferencesNotifier extends AsyncNotifier<UserPreferences> {
  @override
  Future<UserPreferences> build() async {
    final isAuth = await SecureStorage.isAuthenticated();
    if (!isAuth) return const UserPreferences();
    try {
      return await ref.read(authRepositoryProvider).getPreferences();
    } catch (_) {
      return const UserPreferences();
    }
  }

  Future<void> savePreferences(UserPreferences prefs) async {
    state = AsyncData(
      await ref.read(authRepositoryProvider).updatePreferences(prefs),
    );
  }

  Future<void> setOnboardingComplete() async {
    final current = state.valueOrNull ?? const UserPreferences();
    await savePreferences(current.copyWith(onboardingCompleted: true));
  }
}

final preferencesProvider =
    AsyncNotifierProvider<PreferencesNotifier, UserPreferences>(
      PreferencesNotifier.new,
    );

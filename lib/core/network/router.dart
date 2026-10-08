import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/features/auth/data/auth_repository.dart';
import 'package:brewdrift/features/auth/presentation/splash_screen.dart';
import 'package:brewdrift/features/auth/presentation/welcome_screen.dart';
import 'package:brewdrift/features/auth/presentation/login_screen.dart';
import 'package:brewdrift/features/auth/presentation/signup_screen.dart';
import 'package:brewdrift/features/auth/presentation/forgot_password_screen.dart';
import 'package:brewdrift/features/onboarding/presentation/onboarding_screen.dart';
import 'package:brewdrift/features/onboarding/presentation/location_permission_screen.dart';
import 'package:brewdrift/features/home/presentation/home_screen.dart';
import 'package:brewdrift/features/discovery/presentation/explore_screen.dart';
import 'package:brewdrift/features/discovery/presentation/search_screen.dart';
import 'package:brewdrift/features/discovery/presentation/filters_screen.dart';
import 'package:brewdrift/features/map/presentation/map_screen.dart';
import 'package:brewdrift/features/map/presentation/personal_map_screen.dart';
import 'package:brewdrift/features/place_details/presentation/place_details_screen.dart';
import 'package:brewdrift/features/journal/presentation/journal_screen.dart';
import 'package:brewdrift/features/journal/presentation/journal_entry_screen.dart';
import 'package:brewdrift/features/journal/presentation/add_experience_screen.dart';
import 'package:brewdrift/features/journal/presentation/edit_experience_screen.dart';
import 'package:brewdrift/features/favorites/presentation/favorites_screen.dart';
import 'package:brewdrift/features/collections/presentation/collections_screen.dart';
import 'package:brewdrift/features/collections/presentation/collection_details_screen.dart';
import 'package:brewdrift/features/profile/presentation/profile_screen.dart';
import 'package:brewdrift/features/profile/presentation/edit_profile_screen.dart';
import 'package:brewdrift/features/settings/presentation/settings_screen.dart';
import 'package:brewdrift/features/settings/presentation/preferences_screen.dart';
import 'package:brewdrift/features/settings/presentation/privacy_screen.dart';
import 'package:brewdrift/features/settings/presentation/about_screen.dart';
import 'package:brewdrift/shared/widgets/shell_scaffold.dart';

import 'package:brewdrift/core/constants/routes.dart';

final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _shellNavigatorKey = GlobalKey<NavigatorState>();

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: BrewdriftRoutes.splash,
    redirect: (context, state) async {
      final path = state.uri.toString();

      // Always allow splash
      if (path == BrewdriftRoutes.splash) return null;

      // Auth loading — stay on splash
      if (authState.isLoading) return BrewdriftRoutes.splash;

      final isAuth = authState.valueOrNull != null;
      final isOnAuthRoute =
          path.startsWith('/auth') ||
          path == BrewdriftRoutes.welcome ||
          path.startsWith('/onboarding');

      if (!isAuth && !isOnAuthRoute) {
        return BrewdriftRoutes.welcome;
      }

      if (isAuth && isOnAuthRoute) {
        return BrewdriftRoutes.home;
      }

      return null;
    },
    routes: [
      GoRoute(
        path: BrewdriftRoutes.splash,
        builder: (_, __) => const SplashScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.welcome,
        builder: (_, __) => const WelcomeScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.login,
        builder: (_, __) => const LoginScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.signup,
        builder: (_, __) => const SignupScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.forgotPassword,
        builder: (_, __) => const ForgotPasswordScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.onboarding,
        builder: (_, __) => const OnboardingScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.locationPermission,
        builder: (_, __) => const LocationPermissionScreen(),
      ),
      // ── Modals (no bottom nav) ─────────────────────────
      GoRoute(
        path: '/places/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) {
          final placeId = state.pathParameters['id']!;
          final extra = state.extra as Map<String, dynamic>?;
          return PlaceDetailsScreen(placeId: placeId, extra: extra);
        },
      ),
      GoRoute(
        path: '/places/:id/experience',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) {
          final extra = state.extra as Map<String, dynamic>?;
          final placeName = extra?['place_name'] as String? ?? 'Café';
          final placeId = state.pathParameters['id']!;
          return AddExperienceScreen(placeId: placeId, placeName: placeName);
        },
      ),
      GoRoute(
        path: '/visits/:id/edit',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) {
          final visitId = state.pathParameters['id']!;
          return EditExperienceScreen(visitId: visitId);
        },
      ),
      GoRoute(
        path: '/journal/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) {
          final entryId = state.pathParameters['id']!;
          return JournalEntryScreen(visitId: entryId);
        },
      ),
      GoRoute(
        path: BrewdriftRoutes.personalMap,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const PersonalMapScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.search,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const SearchScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.filters,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const FiltersScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.editProfile,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const EditProfileScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.preferences,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const PreferencesScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.privacy,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const PrivacyScreen(),
      ),
      GoRoute(
        path: BrewdriftRoutes.about,
        parentNavigatorKey: _rootNavigatorKey,
        builder: (_, __) => const AboutScreen(),
      ),
      GoRoute(
        path: '/collections/:id',
        parentNavigatorKey: _rootNavigatorKey,
        builder: (context, state) {
          final id = state.pathParameters['id']!;
          return CollectionDetailsScreen(collectionId: id);
        },
      ),
      // ── Shell (bottom nav) ────────────────────────────
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) {
          return ShellScaffold(child: child);
        },
        routes: [
          GoRoute(
            path: BrewdriftRoutes.home,
            builder: (_, __) => const HomeScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.explore,
            builder: (_, __) => const ExploreScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.journal,
            builder: (_, __) => const JournalScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.map,
            builder: (_, __) => const MapScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.profile,
            builder: (_, __) => const ProfileScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.favorites,
            builder: (_, __) => const FavoritesScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.collections,
            builder: (_, __) => const CollectionsScreen(),
          ),
          GoRoute(
            path: BrewdriftRoutes.settings,
            builder: (_, __) => const SettingsScreen(),
          ),
        ],
      ),
    ],
  );
});

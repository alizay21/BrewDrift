import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/routes.dart';
import 'package:brewdrift/core/utils/location_service.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';

class LocationPermissionScreen extends ConsumerStatefulWidget {
  const LocationPermissionScreen({super.key});

  @override
  ConsumerState<LocationPermissionScreen> createState() =>
      _LocationPermissionScreenState();
}

class _LocationPermissionScreenState
    extends ConsumerState<LocationPermissionScreen> {
  bool _isRequesting = false;

  Future<void> _requestPermission() async {
    setState(() => _isRequesting = true);
    try {
      await ref.read(locationProvider.notifier).fetchLocation();
      if (mounted) context.go(BrewdriftRoutes.home);
    } catch (e) {
      if (mounted) {
        final message = e.toString();
        if (message.toLowerCase().contains('permanent')) {
          _showPermanentlyDeniedDialog();
        }
        // If just denied, let them continue to manual search
      }
    } finally {
      if (mounted) setState(() => _isRequesting = false);
    }
  }

  void _showPermanentlyDeniedDialog() {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Location Disabled'),
        content: const Text(
          'Location permission was permanently denied. Enable it in Settings to discover nearby cafés.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(context);
              await ref.read(locationServiceProvider).openSettings();
            },
            child: const Text('Open Settings'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.screenPadding),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('🗺️', style: TextStyle(fontSize: 80)),
              const SizedBox(height: AppSpacing.xl),
              Text(
                'Find cafés\naround you.',
                style: AppTypography.displayMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                'Allow Brewdrift to use your location so we can find the best cafés nearby.',
                style: AppTypography.bodyMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.xl),
              BrewButton(
                text: 'Allow Location',
                onPressed: _requestPermission,
                isLoading: _isRequesting,
              ),
              const SizedBox(height: AppSpacing.md),
              BrewButton(
                text: 'Search Manually Instead',
                onPressed: () => context.go(BrewdriftRoutes.explore),
                isPrimary: false,
              ),
              const SizedBox(height: AppSpacing.lg),
              Text(
                'You can change location access anytime in Settings.',
                style: AppTypography.bodySmall.copyWith(
                  color: AppColors.mochaMedium.withOpacity(0.7),
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

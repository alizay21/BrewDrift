import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';

class BrewErrorState extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;
  final String icon;

  const BrewErrorState({
    Key? key,
    required this.message,
    this.onRetry,
    this.icon = '⚠️',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(icon, style: const TextStyle(fontSize: 48)),
            const SizedBox(height: 24),
            Text(
              'Oops!',
              style: GoogleFonts.playfairDisplay(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.espressoBrown,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              message,
              textAlign: TextAlign.center,
              style: GoogleFonts.dmSans(
                fontSize: 16,
                color: AppColors.mochaMedium,
              ),
            ),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              SizedBox(
                width: 150,
                child: BrewButton(
                  text: 'Retry',
                  onPressed: onRetry,
                  isPrimary: false,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class BrewOfflineState extends StatelessWidget {
  final VoidCallback? onRetry;
  const BrewOfflineState({Key? key, this.onRetry}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BrewErrorState(
      icon: '📡',
      message: 'It seems you are offline. Please check your connection and try again.',
      onRetry: onRetry,
    );
  }
}

class BrewPermissionState extends StatelessWidget {
  final String message;
  final VoidCallback openSettings;

  const BrewPermissionState({
    Key? key,
    required this.message,
    required this.openSettings,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('🗺️', style: TextStyle(fontSize: 48)),
            const SizedBox(height: 24),
            Text(
              'Permission Required',
              style: GoogleFonts.playfairDisplay(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.espressoBrown,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              message,
              textAlign: TextAlign.center,
              style: GoogleFonts.dmSans(
                fontSize: 16,
                color: AppColors.mochaMedium,
              ),
            ),
            const SizedBox(height: 24),
            BrewButton(
              text: 'Open Settings',
              onPressed: openSettings,
            ),
          ],
        ),
      ),
    );
  }
}

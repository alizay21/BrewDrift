import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';

class BrewEmptyState extends StatelessWidget {
  final String icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onAction;

  const BrewEmptyState({
    Key? key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onAction,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              icon,
              style: const TextStyle(fontSize: 64),
            ),
            const SizedBox(height: 24),
            Text(
              title,
              textAlign: TextAlign.center,
              style: GoogleFonts.playfairDisplay(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.espressoBrown,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              subtitle,
              textAlign: TextAlign.center,
              style: GoogleFonts.dmSans(
                fontSize: 16,
                color: AppColors.mochaMedium,
              ),
            ),
            if (actionLabel != null && onAction != null) ...[
              const SizedBox(height: 32),
              SizedBox(
                width: 200,
                child: BrewButton(
                  text: actionLabel!,
                  onPressed: onAction,
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

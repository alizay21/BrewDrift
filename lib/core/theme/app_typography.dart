import 'package:flutter/material.dart';
import 'app_colors.dart';

/// Brewdrift typography system
class AppTypography {
  AppTypography._();

  // ── Font Families ────────────────────────────────────────
  static const String playfair = 'PlayfairDisplay';
  static const String dmSans = 'DMSans';
  static const String cormorant = 'CormorantGaramond';

  // ── Display (Playfair Display) ──────────────────────────
  static const TextStyle displayLarge = TextStyle(
    fontFamily: playfair,
    fontSize: 36,
    fontWeight: FontWeight.w700,
    color: AppColors.espressoBrown,
    height: 1.2,
    letterSpacing: -0.5,
  );

  static const TextStyle displayMedium = TextStyle(
    fontFamily: playfair,
    fontSize: 30,
    fontWeight: FontWeight.w700,
    color: AppColors.espressoBrown,
    height: 1.25,
    letterSpacing: -0.3,
  );

  static const TextStyle displaySmall = TextStyle(
    fontFamily: playfair,
    fontSize: 24,
    fontWeight: FontWeight.w600,
    color: AppColors.espressoBrown,
    height: 1.3,
  );

  // ── Headings (DM Sans) ───────────────────────────────────
  static const TextStyle headingLarge = TextStyle(
    fontFamily: dmSans,
    fontSize: 22,
    fontWeight: FontWeight.w600,
    color: AppColors.espressoBrown,
    height: 1.3,
  );

  static const TextStyle headingMedium = TextStyle(
    fontFamily: dmSans,
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: AppColors.espressoBrown,
    height: 1.35,
  );

  static const TextStyle headingSmall = TextStyle(
    fontFamily: dmSans,
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: AppColors.espressoBrown,
    height: 1.4,
  );

  // ── Body (DM Sans) ───────────────────────────────────────
  static const TextStyle bodyLarge = TextStyle(
    fontFamily: dmSans,
    fontSize: 16,
    fontWeight: FontWeight.w400,
    color: AppColors.espressoBrown,
    height: 1.5,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontFamily: dmSans,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    color: AppColors.mochaMedium,
    height: 1.5,
  );

  static const TextStyle bodySmall = TextStyle(
    fontFamily: dmSans,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.mochaMedium,
    height: 1.5,
  );

  // ── Label / Meta ─────────────────────────────────────────
  static const TextStyle labelLarge = TextStyle(
    fontFamily: dmSans,
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: AppColors.espressoBrown,
    letterSpacing: 0.2,
  );

  static const TextStyle labelMedium = TextStyle(
    fontFamily: dmSans,
    fontSize: 12,
    fontWeight: FontWeight.w500,
    color: AppColors.mochaMedium,
    letterSpacing: 0.3,
  );

  static const TextStyle labelSmall = TextStyle(
    fontFamily: dmSans,
    fontSize: 11,
    fontWeight: FontWeight.w500,
    color: AppColors.mochaMedium,
    letterSpacing: 0.5,
  );

  // ── Caption (Cormorant Garamond) ─────────────────────────
  static const TextStyle caption = TextStyle(
    fontFamily: cormorant,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    fontStyle: FontStyle.italic,
    color: AppColors.mochaMedium,
    height: 1.4,
  );

  static const TextStyle captionLarge = TextStyle(
    fontFamily: cormorant,
    fontSize: 16,
    fontWeight: FontWeight.w400,
    fontStyle: FontStyle.italic,
    color: AppColors.mochaMedium,
    height: 1.4,
  );

  // ── Special ──────────────────────────────────────────────
  static const TextStyle brandLogo = TextStyle(
    fontFamily: playfair,
    fontSize: 42,
    fontWeight: FontWeight.w700,
    color: AppColors.warmCream,
    letterSpacing: 6,
  );

  static const TextStyle brandTagline = TextStyle(
    fontFamily: cormorant,
    fontSize: 16,
    fontWeight: FontWeight.w400,
    fontStyle: FontStyle.italic,
    color: AppColors.parchment,
    letterSpacing: 1.2,
    height: 1.5,
  );

  static const TextStyle buttonText = TextStyle(
    fontFamily: dmSans,
    fontSize: 16,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.3,
    height: 1,
  );

  static const TextStyle buttonSmall = TextStyle(
    fontFamily: dmSans,
    fontSize: 14,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.2,
    height: 1,
  );

  static const TextStyle vibeScore = TextStyle(
    fontFamily: playfair,
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: AppColors.caramel,
    height: 1,
  );

  static const TextStyle price = TextStyle(
    fontFamily: dmSans,
    fontSize: 13,
    fontWeight: FontWeight.w500,
    color: AppColors.mochaMedium,
    letterSpacing: 0.3,
  );

  // ── Numeric display ──────────────────────────────────────
  static const TextStyle statNumber = TextStyle(
    fontFamily: playfair,
    fontSize: 32,
    fontWeight: FontWeight.w700,
    color: AppColors.caramel,
    height: 1,
  );

  static const TextStyle statLabel = TextStyle(
    fontFamily: dmSans,
    fontSize: 11,
    fontWeight: FontWeight.w400,
    color: AppColors.mochaMedium,
    letterSpacing: 0.5,
    height: 1.2,
  );
}

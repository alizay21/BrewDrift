import 'package:flutter/material.dart';

/// Brewdrift color palette — warm, cozy, sophisticated
class AppColors {
  AppColors._();

  // ── Core Backgrounds ────────────────────────────────────
  static const Color warmCream = Color(0xFFF5EDD8);
  static const Color parchment = Color(0xFFEDE0C4);
  static const Color softBeige = Color(0xFFFAF3E7);
  static const Color offWhite = Color(0xFFFFFBF2);

  // ── Brand ────────────────────────────────────────────────
  static const Color espressoBrown = Color(0xFF2C1A0E);
  static const Color darkRoast = Color(0xFF1A0E08);
  static const Color mochaMedium = Color(0xFF7A4A2E);

  // ── Accents ──────────────────────────────────────────────
  static const Color caramel = Color(0xFFC47C3A);
  static const Color mutedGold = Color(0xFFC9A84C);
  static const Color terracotta = Color(0xFFC4704A);
  static const Color sageGreen = Color(0xFF8B9E81);

  // ── Functional ───────────────────────────────────────────
  static const Color error = Color(0xFFB5451B);
  static const Color success = Color(0xFF6A8F5E);
  static const Color warning = Color(0xFFD4940A);
  static const Color divider = Color(0xFFE5D9C4);
  static const Color shimmerBase = Color(0xFFEDE0C4);
  static const Color shimmerHighlight = Color(0xFFF5EDD8);

  // ── Transparent overlays ─────────────────────────────────
  static Color espressoOverlay(double opacity) =>
      espressoBrown.withValues(alpha: opacity);
  static Color caramelOverlay(double opacity) => caramel.withValues(alpha: opacity);

  // ── Gradient definitions ─────────────────────────────────
  static const LinearGradient splashGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [darkRoast, Color(0xFF3D2214)],
  );

  static const LinearGradient warmGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [softBeige, warmCream],
  );

  static const LinearGradient cardGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [Colors.transparent, Color(0xCC1A0E08)],
  );

  // ── Vibe colors ──────────────────────────────────────────
  static const Color vibeCozy = Color(0xFFC47C3A);
  static const Color vibeNature = Color(0xFF8B9E81);
  static const Color vibeCute = Color(0xFFE8A598);
  static const Color vibeVintage = Color(0xFFB8955A);
  static const Color vibeDark = Color(0xFF4A3040);
  static const Color vibeStudy = Color(0xFF6B8CAE);
  static const Color vibeDate = Color(0xFFD4849A);
  static const Color vibeFancy = Color(0xFFC9A84C);
  static const Color vibeOutdoor = Color(0xFF7BA77B);
  static const Color vibeBookish = Color(0xFF8B7355);
  static const Color vibeArtsy = Color(0xFFB5734A);
  static const Color vibeMinimal = Color(0xFF9EB0A0);
}

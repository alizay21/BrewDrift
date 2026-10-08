import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'app_colors.dart';
import 'app_typography.dart';
import 'app_spacing.dart';
import 'app_radius.dart';

/// Brewdrift Material 3 theme — warm, cozy, premium
class AppTheme {
  AppTheme._();

  static ThemeData get light {
    return ThemeData(
      useMaterial3: true,
      colorScheme: _colorScheme,
      scaffoldBackgroundColor: AppColors.softBeige,
      fontFamily: AppTypography.dmSans,
      appBarTheme: _appBarTheme,
      elevatedButtonTheme: _elevatedButtonTheme,
      outlinedButtonTheme: _outlinedButtonTheme,
      textButtonTheme: _textButtonTheme,
      inputDecorationTheme: _inputDecorationTheme,
      bottomNavigationBarTheme: _bottomNavTheme,
      chipTheme: _chipTheme,
      cardTheme: _cardTheme,
      floatingActionButtonTheme: _fabTheme,
      snackBarTheme: _snackBarTheme,
      dividerTheme: _dividerTheme,
      textTheme: _textTheme,
      iconTheme: _iconTheme,
      bottomSheetTheme: _bottomSheetTheme,
      dialogTheme: _dialogTheme,
      switchTheme: _switchTheme,
      checkboxTheme: _checkboxTheme,
      listTileTheme: _listTileTheme,
      navigationBarTheme: _navigationBarTheme,
      splashColor: AppColors.caramelOverlay(0.08),
      highlightColor: AppColors.caramelOverlay(0.04),
    );
  }

  static ColorScheme get _colorScheme {
    return const ColorScheme(
      brightness: Brightness.light,
      primary: AppColors.caramel,
      onPrimary: AppColors.offWhite,
      primaryContainer: AppColors.warmCream,
      onPrimaryContainer: AppColors.espressoBrown,
      secondary: AppColors.mochaMedium,
      onSecondary: AppColors.offWhite,
      secondaryContainer: AppColors.parchment,
      onSecondaryContainer: AppColors.espressoBrown,
      tertiary: AppColors.sageGreen,
      onTertiary: AppColors.offWhite,
      tertiaryContainer: Color(0xFFD4E4CF),
      onTertiaryContainer: AppColors.espressoBrown,
      error: AppColors.error,
      onError: AppColors.offWhite,
      errorContainer: Color(0xFFFFDAD6),
      onErrorContainer: AppColors.espressoBrown,
      surface: AppColors.softBeige,
      onSurface: AppColors.espressoBrown,
      surfaceContainerHighest: AppColors.parchment,
      onSurfaceVariant: AppColors.mochaMedium,
      outline: AppColors.divider,
      outlineVariant: Color(0xFFF0E6D3),
      shadow: AppColors.espressoBrown,
      scrim: Color(0x80000000),
      inverseSurface: AppColors.espressoBrown,
      onInverseSurface: AppColors.warmCream,
      inversePrimary: AppColors.mutedGold,
    );
  }

  static AppBarTheme get _appBarTheme {
    return const AppBarTheme(
      backgroundColor: AppColors.softBeige,
      foregroundColor: AppColors.espressoBrown,
      elevation: 0,
      scrolledUnderElevation: 0,
      centerTitle: false,
      titleTextStyle: AppTypography.headingMedium,
      iconTheme: IconThemeData(color: AppColors.espressoBrown, size: 24),
      actionsIconTheme: IconThemeData(color: AppColors.mochaMedium, size: 24),
      systemOverlayStyle: SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
        statusBarBrightness: Brightness.light,
      ),
    );
  }

  static ElevatedButtonThemeData get _elevatedButtonTheme {
    return ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.caramel,
        foregroundColor: AppColors.offWhite,
        elevation: 0,
        shadowColor: Colors.transparent,
        textStyle: AppTypography.buttonText,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.lg,
          vertical: AppSpacing.md,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.button),
        ),
        minimumSize: const Size(double.infinity, 52),
      ),
    );
  }

  static OutlinedButtonThemeData get _outlinedButtonTheme {
    return OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: AppColors.caramel,
        side: const BorderSide(color: AppColors.caramel, width: 1.5),
        textStyle: AppTypography.buttonText,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.lg,
          vertical: AppSpacing.md,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadius.button),
        ),
        minimumSize: const Size(double.infinity, 52),
      ),
    );
  }

  static TextButtonThemeData get _textButtonTheme {
    return TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: AppColors.caramel,
        textStyle: AppTypography.labelLarge,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.sm,
          vertical: AppSpacing.xs,
        ),
      ),
    );
  }

  static InputDecorationTheme get _inputDecorationTheme {
    return InputDecorationTheme(
      filled: true,
      fillColor: AppColors.warmCream,
      hintStyle: AppTypography.bodyMedium.copyWith(
        color: AppColors.mochaMedium.withOpacity(0.6),
      ),
      labelStyle: AppTypography.labelLarge,
      floatingLabelStyle: AppTypography.labelMedium.copyWith(
        color: AppColors.caramel,
      ),
      errorStyle: AppTypography.bodySmall.copyWith(color: AppColors.error),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.md,
      ),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.input),
        borderSide: const BorderSide(color: AppColors.divider),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.input),
        borderSide: const BorderSide(color: AppColors.divider, width: 1),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.input),
        borderSide: const BorderSide(color: AppColors.caramel, width: 1.5),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.input),
        borderSide: const BorderSide(color: AppColors.error, width: 1),
      ),
      focusedErrorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.input),
        borderSide: const BorderSide(color: AppColors.error, width: 1.5),
      ),
      prefixIconColor: AppColors.mochaMedium,
      suffixIconColor: AppColors.mochaMedium,
    );
  }

  static BottomNavigationBarThemeData get _bottomNavTheme {
    return const BottomNavigationBarThemeData(
      backgroundColor: AppColors.offWhite,
      selectedItemColor: AppColors.caramel,
      unselectedItemColor: AppColors.mochaMedium,
      selectedLabelStyle: TextStyle(
        fontFamily: AppTypography.dmSans,
        fontSize: 11,
        fontWeight: FontWeight.w600,
      ),
      unselectedLabelStyle: TextStyle(
        fontFamily: AppTypography.dmSans,
        fontSize: 11,
        fontWeight: FontWeight.w400,
      ),
      type: BottomNavigationBarType.fixed,
      elevation: 8,
      showSelectedLabels: true,
      showUnselectedLabels: true,
    );
  }

  static NavigationBarThemeData get _navigationBarTheme {
    return NavigationBarThemeData(
      backgroundColor: AppColors.offWhite,
      indicatorColor: AppColors.caramel.withOpacity(0.15),
      iconTheme: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return const IconThemeData(color: AppColors.caramel, size: 24);
        }
        return const IconThemeData(color: AppColors.mochaMedium, size: 24);
      }),
      labelTextStyle: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return const TextStyle(
            fontFamily: AppTypography.dmSans,
            fontSize: 11,
            fontWeight: FontWeight.w600,
            color: AppColors.caramel,
          );
        }
        return const TextStyle(
          fontFamily: AppTypography.dmSans,
          fontSize: 11,
          fontWeight: FontWeight.w400,
          color: AppColors.mochaMedium,
        );
      }),
      elevation: 8,
      height: 72,
    );
  }

  static ChipThemeData get _chipTheme {
    return ChipThemeData(
      backgroundColor: AppColors.warmCream,
      selectedColor: AppColors.caramel,
      side: const BorderSide(color: AppColors.divider),
      labelStyle: AppTypography.labelMedium,
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      shape: const StadiumBorder(),
    );
  }

  static CardThemeData get _cardTheme {
    return CardThemeData(
      color: AppColors.offWhite,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.card),
      ),
      margin: EdgeInsets.zero,
    );
  }

  static FloatingActionButtonThemeData get _fabTheme {
    return const FloatingActionButtonThemeData(
      backgroundColor: AppColors.caramel,
      foregroundColor: AppColors.offWhite,
      elevation: 4,
      shape: CircleBorder(),
    );
  }

  static SnackBarThemeData get _snackBarTheme {
    return SnackBarThemeData(
      backgroundColor: AppColors.espressoBrown,
      contentTextStyle: AppTypography.bodyMedium.copyWith(
        color: AppColors.warmCream,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.sm),
      ),
      behavior: SnackBarBehavior.floating,
    );
  }

  static DividerThemeData get _dividerTheme {
    return const DividerThemeData(
      color: AppColors.divider,
      thickness: 1,
      space: 1,
    );
  }

  static TextTheme get _textTheme {
    return const TextTheme(
      displayLarge: AppTypography.displayLarge,
      displayMedium: AppTypography.displayMedium,
      displaySmall: AppTypography.displaySmall,
      headlineLarge: AppTypography.headingLarge,
      headlineMedium: AppTypography.headingMedium,
      headlineSmall: AppTypography.headingSmall,
      bodyLarge: AppTypography.bodyLarge,
      bodyMedium: AppTypography.bodyMedium,
      bodySmall: AppTypography.bodySmall,
      labelLarge: AppTypography.labelLarge,
      labelMedium: AppTypography.labelMedium,
      labelSmall: AppTypography.labelSmall,
    );
  }

  static IconThemeData get _iconTheme {
    return const IconThemeData(color: AppColors.espressoBrown, size: 24);
  }

  static BottomSheetThemeData get _bottomSheetTheme {
    return const BottomSheetThemeData(
      backgroundColor: AppColors.softBeige,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(AppRadius.bottomSheet),
        ),
      ),
      dragHandleColor: AppColors.divider,
      dragHandleSize: Size(40, 4),
    );
  }

  static DialogThemeData get _dialogTheme {
    return const DialogThemeData(
      backgroundColor: AppColors.softBeige,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(AppRadius.lg)),
      ),
      titleTextStyle: AppTypography.headingMedium,
      contentTextStyle: AppTypography.bodyMedium,
    );
  }

  static SwitchThemeData get _switchTheme {
    return SwitchThemeData(
      thumbColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) return AppColors.caramel;
        return AppColors.divider;
      }),
      trackColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return AppColors.caramel.withOpacity(0.3);
        }
        return AppColors.divider;
      }),
    );
  }

  static CheckboxThemeData get _checkboxTheme {
    return CheckboxThemeData(
      fillColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) return AppColors.caramel;
        return Colors.transparent;
      }),
      checkColor: WidgetStateProperty.all(AppColors.offWhite),
      side: const BorderSide(color: AppColors.divider, width: 1.5),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
    );
  }

  static ListTileThemeData get _listTileTheme {
    return const ListTileThemeData(
      contentPadding: EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.xs,
      ),
      iconColor: AppColors.mochaMedium,
      textColor: AppColors.espressoBrown,
      titleTextStyle: AppTypography.bodyLarge,
      subtitleTextStyle: AppTypography.bodySmall,
    );
  }
}

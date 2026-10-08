import os

files = {
    "lib/shared/widgets/brew_button.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';

class BrewButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final bool isPrimary;

  const BrewButton({
    Key? key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.isPrimary = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 52,
      child: isPrimary
          ? ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.caramel,
                foregroundColor: AppColors.offWhite,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                elevation: 0,
              ),
              onPressed: isLoading ? null : onPressed,
              child: _buildChild(),
            )
          : OutlinedButton(
              style: OutlinedButton.styleFrom(
                foregroundColor: AppColors.caramel,
                side: const BorderSide(color: AppColors.caramel, width: 1.5),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              onPressed: isLoading ? null : onPressed,
              child: _buildChild(),
            ),
    );
  }

  Widget _buildChild() {
    if (isLoading) {
      return SizedBox(
        height: 24,
        width: 24,
        child: CircularProgressIndicator(
          strokeWidth: 2.5,
          color: isPrimary ? AppColors.offWhite : AppColors.caramel,
        ),
      );
    }
    return Text(
      text,
      style: GoogleFonts.dmSans(
        fontSize: 16,
        fontWeight: FontWeight.w600,
      ),
    );
  }
}
""",
    "lib/shared/widgets/brew_text_field.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';

class BrewTextField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String hint;
  final String? Function(String?)? validator;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final bool obscureText;
  final TextInputType keyboardType;
  final TextInputAction textInputAction;
  final void Function(String)? onFieldSubmitted;
  final int maxLines;

  const BrewTextField({
    Key? key,
    required this.controller,
    required this.label,
    required this.hint,
    this.validator,
    this.prefixIcon,
    this.suffixIcon,
    this.obscureText = false,
    this.keyboardType = TextInputType.text,
    this.textInputAction = TextInputAction.next,
    this.onFieldSubmitted,
    this.maxLines = 1,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (label.isNotEmpty) ...[
          Text(
            label,
            style: GoogleFonts.dmSans(
              fontSize: 14,
              fontWeight: FontWeight.w500,
              color: AppColors.espressoBrown,
            ),
          ),
          const SizedBox(height: 8),
        ],
        TextFormField(
          controller: controller,
          validator: validator,
          obscureText: obscureText,
          keyboardType: keyboardType,
          textInputAction: textInputAction,
          onFieldSubmitted: onFieldSubmitted,
          maxLines: maxLines,
          style: GoogleFonts.dmSans(
            fontSize: 16,
            color: AppColors.espressoBrown,
          ),
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: GoogleFonts.dmSans(
              color: AppColors.mochaMedium.withOpacity(0.5),
            ),
            filled: true,
            fillColor: AppColors.warmCream,
            prefixIcon: prefixIcon,
            suffixIcon: suffixIcon,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide.none,
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: const BorderSide(
                color: AppColors.espressoBrown,
                width: 1.5,
              ),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: const BorderSide(
                color: AppColors.terracotta,
                width: 1.5,
              ),
            ),
            focusedErrorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: const BorderSide(
                color: AppColors.terracotta,
                width: 1.5,
              ),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 16,
            ),
          ),
        ),
      ],
    );
  }
}
""",
    "lib/shared/widgets/brew_snackbar.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';

class BrewSnackbar {
  static void show(
    BuildContext context,
    String message, {
    bool isError = false,
    bool isSuccess = false,
  }) {
    Color backgroundColor = AppColors.darkRoast;
    Color textColor = AppColors.offWhite;

    if (isError) {
      backgroundColor = AppColors.espressoBrown;
      textColor = AppColors.warmCream;
    } else if (isSuccess) {
      backgroundColor = AppColors.caramel;
      textColor = AppColors.offWhite;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          message,
          style: GoogleFonts.dmSans(
            color: textColor,
            fontSize: 14,
            fontWeight: FontWeight.w500,
          ),
        ),
        backgroundColor: backgroundColor,
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        margin: const EdgeInsets.all(16),
        duration: const Duration(seconds: 3),
      ),
    );
  }
}
""",
    "lib/shared/widgets/brew_app_bar.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';

class BrewAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final bool showBack;
  final List<Widget>? actions;
  final VoidCallback? onBack;

  const BrewAppBar({
    Key? key,
    required this.title,
    this.showBack = true,
    this.actions,
    this.onBack,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      centerTitle: true,
      leading: showBack
          ? IconButton(
              icon: const Icon(
                Icons.arrow_back_ios_new_rounded,
                color: AppColors.espressoBrown,
                size: 20,
              ),
              onPressed: onBack ?? () => context.pop(),
            )
          : null,
      title: Text(
        title,
        style: GoogleFonts.playfairDisplay(
          color: AppColors.espressoBrown,
          fontSize: 20,
          fontWeight: FontWeight.w600,
        ),
      ),
      actions: actions,
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
""",
    "lib/shared/widgets/cafe_card.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/shared/widgets/loading_state.dart';

class CafeCard extends StatelessWidget {
  final Place place;
  final bool isHorizontal;
  final double? vibeMatch;

  const CafeCard({
    Key? key,
    required this.place,
    this.isHorizontal = false,
    this.vibeMatch,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.push('/place/${place.id}', extra: place);
      },
      child: Container(
        width: isHorizontal ? 260 : double.infinity,
        margin: EdgeInsets.only(
          right: isHorizontal ? 16 : 0,
          bottom: isHorizontal ? 0 : 16,
        ),
        decoration: BoxDecoration(
          color: AppColors.offWhite,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: AppColors.espressoBrown.withOpacity(0.08),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                  child: CachedNetworkImage(
                    imageUrl: place.photoUrl ?? 'https://via.placeholder.com/400x200',
                    height: isHorizontal ? 140 : 180,
                    width: double.infinity,
                    fit: BoxFit.cover,
                    placeholder: (context, url) => const ShimmerWidget(height: 180, width: double.infinity),
                    errorWidget: (context, url, error) => Container(
                      height: isHorizontal ? 140 : 180,
                      width: double.infinity,
                      color: AppColors.warmCream,
                      child: const Icon(Icons.local_cafe, color: AppColors.caramel, size: 40),
                    ),
                  ),
                ),
                if (place.isOpen != null)
                  Positioned(
                    top: 12,
                    right: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: place.isOpen! ? AppColors.sageGreen : AppColors.terracotta,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        place.isOpen! ? 'OPEN' : 'CLOSED',
                        style: GoogleFonts.dmSans(
                          color: AppColors.offWhite,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                if (vibeMatch != null)
                  Positioned(
                    top: 12,
                    left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppColors.mutedGold,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        '${(vibeMatch! * 100).toInt()}% Match',
                        style: GoogleFonts.dmSans(
                          color: AppColors.darkRoast,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    place.name,
                    style: GoogleFonts.playfairDisplay(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppColors.espressoBrown,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.star_rounded, color: AppColors.mutedGold, size: 18),
                      const SizedBox(width: 4),
                      Text(
                        place.rating?.toStringAsFixed(1) ?? 'N/A',
                        style: GoogleFonts.dmSans(
                          fontWeight: FontWeight.w600,
                          color: AppColors.espressoBrown,
                        ),
                      ),
                      const SizedBox(width: 4),
                      Text(
                        '(${place.userRatingsTotal ?? 0})',
                        style: GoogleFonts.dmSans(
                          color: AppColors.mochaMedium,
                          fontSize: 12,
                        ),
                      ),
                      const Spacer(),
                      if (place.distance != null) ...[
                        const Icon(Icons.location_on_outlined, color: AppColors.caramel, size: 16),
                        const SizedBox(width: 4),
                        Text(
                          '${place.distance!.toStringAsFixed(1)} km',
                          style: GoogleFonts.dmSans(
                            color: AppColors.mochaMedium,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
""",
    "lib/shared/widgets/vibe_chip.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:brewdrift/shared/models/models.dart';

class VibeChip extends StatelessWidget {
  final VibeDefinition vibe;
  final bool isSelected;
  final VoidCallback onTap;

  const VibeChip({
    Key? key,
    required this.vibe,
    required this.isSelected,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: isSelected ? AppColors.caramel : AppColors.warmCream,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? AppColors.caramel : AppColors.divider,
            width: 1,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              vibe.icon,
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(width: 8),
            Text(
              vibe.name,
              style: GoogleFonts.dmSans(
                color: isSelected ? AppColors.offWhite : AppColors.espressoBrown,
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
              ),
            ),
          ],
        ),
      ).animate(target: isSelected ? 1 : 0).scaleXY(end: 1.05, duration: 150.ms),
    );
  }
}
""",
    "lib/shared/widgets/star_rating.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';

class StarRating extends StatelessWidget {
  final double rating;
  final double size;
  final Color? color;
  final bool showText;

  const StarRating({
    Key? key,
    required this.rating,
    this.size = 18,
    this.color,
    this.showText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final activeColor = color ?? AppColors.mutedGold;
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(5, (index) {
            if (index < rating.floor()) {
              return Icon(Icons.star_rounded, color: activeColor, size: size);
            } else if (index == rating.floor() && rating % 1 != 0) {
              return Icon(Icons.star_half_rounded, color: activeColor, size: size);
            } else {
              return Icon(Icons.star_outline_rounded, color: AppColors.divider, size: size);
            }
          }),
        ),
        if (showText) ...[
          const SizedBox(width: 8),
          Text(
            rating.toStringAsFixed(1),
            style: GoogleFonts.dmSans(
              fontSize: size * 0.8,
              fontWeight: FontWeight.w600,
              color: AppColors.espressoBrown,
            ),
          ),
        ]
      ],
    );
  }
}

class BrewRatingPicker extends StatefulWidget {
  final int initialRating;
  final ValueChanged<int> onRatingChanged;

  const BrewRatingPicker({
    Key? key,
    this.initialRating = 0,
    required this.onRatingChanged,
  }) : super(key: key);

  @override
  State<BrewRatingPicker> createState() => _BrewRatingPickerState();
}

class _BrewRatingPickerState extends State<BrewRatingPicker> {
  late int _rating;

  @override
  void initState() {
    super.initState();
    _rating = widget.initialRating;
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (index) {
        return GestureDetector(
          onTap: () {
            setState(() {
              _rating = index + 1;
            });
            widget.onRatingChanged(_rating);
          },
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: Icon(
              index < _rating ? Icons.star_rounded : Icons.star_outline_rounded,
              color: index < _rating ? AppColors.mutedGold : AppColors.divider,
              size: 40,
            ),
          ),
        );
      }),
    );
  }
}
""",
    "lib/shared/widgets/loading_state.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:flutter_animate/flutter_animate.dart';

class BrewLoadingState extends StatelessWidget {
  final String? message;
  
  const BrewLoadingState({Key? key, this.message}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(
            color: AppColors.caramel,
          ),
          if (message != null) ...[
            const SizedBox(height: 16),
            Text(
              message!,
              style: const TextStyle(
                color: AppColors.mochaMedium,
                fontSize: 16,
              ),
            ),
          ]
        ],
      ),
    );
  }
}

class CafeCardSkeleton extends StatelessWidget {
  final bool isHorizontal;
  const CafeCardSkeleton({Key? key, this.isHorizontal = false}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: isHorizontal ? 260 : double.infinity,
      margin: EdgeInsets.only(
        right: isHorizontal ? 16 : 0,
        bottom: isHorizontal ? 0 : 16,
      ),
      decoration: BoxDecoration(
        color: AppColors.offWhite,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const ShimmerWidget(
            height: 180,
            width: double.infinity,
            borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                ShimmerWidget(height: 20, width: 150),
                SizedBox(height: 8),
                ShimmerWidget(height: 16, width: 200),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ShimmerWidget extends StatelessWidget {
  final double height;
  final double width;
  final BorderRadius? borderRadius;

  const ShimmerWidget({
    Key? key,
    required this.height,
    required this.width,
    this.borderRadius,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        color: AppColors.warmCream,
        borderRadius: borderRadius ?? BorderRadius.circular(8),
      ),
    ).animate(onPlay: (controller) => controller.repeat())
     .shimmer(
       duration: const Duration(milliseconds: 1500),
       color: AppColors.parchment.withOpacity(0.5),
     );
  }
}
""",
    "lib/shared/widgets/empty_state.dart": """import 'package:flutter/material.dart';
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
""",
    "lib/shared/widgets/error_state.dart": """import 'package:flutter/material.dart';
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
""",
    "lib/shared/widgets/shell_scaffold.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:go_router/go_router.dart';

class ShellScaffold extends StatelessWidget {
  final Widget child;

  const ShellScaffold({Key? key, required this.child}) : super(key: key);

  int _calculateSelectedIndex(BuildContext context) {
    final String location = GoRouterState.of(context).uri.path;
    if (location.startsWith('/home')) return 0;
    if (location.startsWith('/explore')) return 1;
    if (location.startsWith('/journal')) return 2;
    if (location.startsWith('/map')) return 3;
    if (location.startsWith('/profile')) return 4;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.go('/home');
        break;
      case 1:
        context.go('/explore');
        break;
      case 2:
        context.go('/journal');
        break;
      case 3:
        context.go('/map');
        break;
      case 4:
        context.go('/profile');
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentIndex = _calculateSelectedIndex(context);

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: child,
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          border: Border(
            top: BorderSide(color: AppColors.divider, width: 1),
          ),
        ),
        child: NavigationBar(
          selectedIndex: currentIndex,
          onDestinationSelected: (index) => _onItemTapped(index, context),
          backgroundColor: AppColors.offWhite,
          indicatorColor: AppColors.caramel.withOpacity(0.2),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.home_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.home_rounded, color: AppColors.caramel),
              label: 'Home',
            ),
            NavigationDestination(
              icon: Icon(Icons.search_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.search_rounded, color: AppColors.caramel),
              label: 'Explore',
            ),
            NavigationDestination(
              icon: Icon(Icons.book_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.book_rounded, color: AppColors.caramel),
              label: 'Journal',
            ),
            NavigationDestination(
              icon: Icon(Icons.map_outlined, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.map_rounded, color: AppColors.caramel),
              label: 'Map',
            ),
            NavigationDestination(
              icon: Icon(Icons.person_outline, color: AppColors.mochaMedium),
              selectedIcon: Icon(Icons.person_rounded, color: AppColors.caramel),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}
""",
    "lib/features/auth/presentation/forgot_password_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/brew_snackbar.dart';
import 'package:google_fonts/google_fonts.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({Key? key}) : super(key: key);

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _emailController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      // Mock API call
      await Future.delayed(const Duration(seconds: 1));
      setState(() => _isLoading = false);
      if (mounted) {
        BrewSnackbar.show(context, 'Check your email for reset instructions.', isSuccess: true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'Reset Password'),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Forgot your password?',
                style: GoogleFonts.playfairDisplay(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: AppColors.espressoBrown,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Enter your email address and we will send you instructions to reset your password.',
                style: GoogleFonts.dmSans(
                  fontSize: 16,
                  color: AppColors.mochaMedium,
                ),
              ),
              const SizedBox(height: 32),
              BrewTextField(
                controller: _emailController,
                label: 'Email',
                hint: 'Enter your email',
                keyboardType: TextInputType.emailAddress,
                validator: (val) => val == null || val.isEmpty ? 'Email is required' : null,
              ),
              const SizedBox(height: 32),
              BrewButton(
                text: 'Send Reset Link',
                isLoading: _isLoading,
                onPressed: _submit,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
""",
    "lib/features/onboarding/presentation/onboarding_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/vibe_chip.dart';
import 'package:brewdrift/shared/models/models.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({Key? key}) : super(key: key);

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;
  final List<String> _selectedVibes = [];

  final List<VibeDefinition> allVibes = [
    VibeDefinition(id: 'quiet', name: 'Quiet', icon: '🤫'),
    VibeDefinition(id: 'cozy', name: 'Cozy', icon: '🛋️'),
    VibeDefinition(id: 'lively', name: 'Lively', icon: '🎉'),
    VibeDefinition(id: 'aesthetic', name: 'Aesthetic', icon: '✨'),
    VibeDefinition(id: 'work_friendly', name: 'Work Friendly', icon: '💻'),
    VibeDefinition(id: 'outdoor', name: 'Outdoor', icon: '🌳'),
  ];

  void _nextPage() {
    if (_currentPage < 3) {
      _pageController.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    } else {
      _finishOnboarding();
    }
  }

  void _finishOnboarding() {
    context.go('/home');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.warmCream,
      body: SafeArea(
        child: Column(
          children: [
            Align(
              alignment: Alignment.topRight,
              child: TextButton(
                onPressed: _finishOnboarding,
                child: const Text('Skip', style: TextStyle(color: AppColors.mochaMedium)),
              ),
            ),
            Expanded(
              child: PageView(
                controller: _pageController,
                onPageChanged: (index) => setState(() => _currentPage = index),
                children: [
                  _buildPage1(),
                  _buildPage2(),
                  _buildPage3(),
                  _buildPage4(),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: List.generate(4, (index) {
                      return Container(
                        margin: const EdgeInsets.only(right: 8),
                        height: 8,
                        width: _currentPage == index ? 24 : 8,
                        decoration: BoxDecoration(
                          color: _currentPage == index ? AppColors.caramel : AppColors.divider,
                          borderRadius: BorderRadius.circular(4),
                        ),
                      );
                    }),
                  ),
                  SizedBox(
                    width: 120,
                    child: BrewButton(
                      text: _currentPage == 3 ? 'Done' : 'Next',
                      onPressed: _nextPage,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPage1() {
    return _buildBasePage(
      icon: '☕',
      title: 'Welcome to Brewdrift',
      subtitle: 'Discover, experience, and journal your café moments.',
    );
  }

  Widget _buildPage2() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('✨', style: TextStyle(fontSize: 64)),
          const SizedBox(height: 24),
          Text(
            'Tell us your vibe',
            style: GoogleFonts.playfairDisplay(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.espressoBrown),
          ),
          const SizedBox(height: 12),
          Text(
            'Select the atmospheres you enjoy most.',
            style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.mochaMedium),
          ),
          const SizedBox(height: 32),
          Wrap(
            spacing: 8,
            runSpacing: 12,
            alignment: WrapAlignment.center,
            children: allVibes.map((vibe) {
              final isSelected = _selectedVibes.contains(vibe.id);
              return VibeChip(
                vibe: vibe,
                isSelected: isSelected,
                onTap: () {
                  setState(() {
                    if (isSelected) {
                      _selectedVibes.remove(vibe.id);
                    } else {
                      _selectedVibes.add(vibe.id);
                    }
                  });
                },
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildPage3() {
    return _buildBasePage(
      icon: '🗺️',
      title: 'Let us find cafés around you',
      subtitle: 'Enable location services to discover nearby hidden gems.',
    );
  }

  Widget _buildPage4() {
    return _buildBasePage(
      icon: '📖',
      title: 'Keep your café story',
      subtitle: 'Log your visits, rate your coffee, and save memories.',
    );
  }

  Widget _buildBasePage({required String icon, required String title, required String subtitle}) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(icon, style: const TextStyle(fontSize: 80)),
          const SizedBox(height: 32),
          Text(
            title,
            textAlign: TextAlign.center,
            style: GoogleFonts.playfairDisplay(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.espressoBrown),
          ),
          const SizedBox(height: 16),
          Text(
            subtitle,
            textAlign: TextAlign.center,
            style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.mochaMedium),
          ),
        ],
      ),
    );
  }
}
""",
    "lib/features/onboarding/presentation/location_permission_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:go_router/go_router.dart';

class LocationPermissionScreen extends StatelessWidget {
  const LocationPermissionScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('🗺️', style: TextStyle(fontSize: 80)),
              const SizedBox(height: 32),
              Text(
                'Find cafés around you',
                textAlign: TextAlign.center,
                style: GoogleFonts.playfairDisplay(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: AppColors.espressoBrown,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Brewdrift needs your location to recommend the best spots nearby. We only use your location while you are using the app.',
                textAlign: TextAlign.center,
                style: GoogleFonts.dmSans(
                  fontSize: 16,
                  color: AppColors.mochaMedium,
                ),
              ),
              const SizedBox(height: 48),
              BrewButton(
                text: 'Allow Location',
                onPressed: () {
                  // Mock allow and pop
                  context.pop();
                },
              ),
              const SizedBox(height: 16),
              BrewButton(
                text: 'Search manually',
                isPrimary: false,
                onPressed: () {
                  context.go('/explore');
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
""",
    "lib/features/home/presentation/home_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/cafe_card.dart';
import 'package:brewdrift/shared/models/models.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final TextEditingController _moodController = TextEditingController();

    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async {
            await Future.delayed(const Duration(seconds: 1));
          },
          color: AppColors.caramel,
          child: ListView(
            padding: const EdgeInsets.all(24.0),
            children: [
              Text(
                'Good morning, Alex',
                style: GoogleFonts.playfairDisplay(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: AppColors.espressoBrown,
                ),
              ),
              const SizedBox(height: 32),
              Text(
                '☕ What are you in the mood for?',
                style: GoogleFonts.dmSans(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  color: AppColors.espressoBrown,
                ),
              ),
              const SizedBox(height: 16),
              BrewTextField(
                controller: _moodController,
                label: '',
                hint: 'Describe your mood (e.g. quiet place to read)',
                maxLines: 2,
              ),
              const SizedBox(height: 16),
              BrewButton(
                text: 'Find Cafés',
                onPressed: () {},
              ),
              const SizedBox(height: 40),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Near You',
                    style: GoogleFonts.playfairDisplay(
                      fontSize: 22,
                      fontWeight: FontWeight.w600,
                      color: AppColors.espressoBrown,
                    ),
                  ),
                  Text(
                    'See All',
                    style: GoogleFonts.dmSans(
                      color: AppColors.caramel,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              SizedBox(
                height: 250,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: 3,
                  itemBuilder: (context, index) {
                    return CafeCard(
                      isHorizontal: true,
                      place: Place(
                        id: index.toString(),
                        name: 'Mock Cafe \${index + 1}',
                        lat: 0,
                        lng: 0,
                        rating: 4.5,
                        userRatingsTotal: 120,
                        distance: 1.2,
                        isOpen: true,
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 1 created")

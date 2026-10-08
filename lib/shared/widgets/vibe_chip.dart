import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/core/constants/vibe_definitions.dart';

class VibeChip extends StatelessWidget {
  const VibeChip({
    super.key,
    required this.vibe,
    required this.isSelected,
    required this.onTap,
    this.large = false,
  });

  final VibeDefinition vibe;
  final bool isSelected;
  final VoidCallback onTap;
  final bool large;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedScale(
        scale: isSelected ? 1.04 : 1.0,
        duration: const Duration(milliseconds: 150),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
          padding: EdgeInsets.symmetric(
            horizontal: large ? 16 : 12,
            vertical: large ? 10 : 8,
          ),
          decoration: BoxDecoration(
            color: isSelected ? vibe.color : AppColors.warmCream,
            borderRadius: BorderRadius.circular(AppRadius.full),
            border: Border.all(
              color: isSelected ? vibe.color : AppColors.divider,
              width: isSelected ? 0 : 1,
            ),
            boxShadow: isSelected
                ? [
                    BoxShadow(
                      color: vibe.color.withValues(alpha: 0.25),
                      blurRadius: 8,
                      offset: const Offset(0, 3),
                    ),
                  ]
                : null,
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(vibe.icon, style: TextStyle(fontSize: large ? 18 : 15)),
              const SizedBox(width: 6),
              Text(
                vibe.name,
                style: (large ? AppTypography.labelLarge : AppTypography.labelMedium).copyWith(
                  color: isSelected ? Colors.white : AppColors.espressoBrown,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

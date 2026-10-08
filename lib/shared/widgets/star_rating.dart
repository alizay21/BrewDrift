import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';

class StarRating extends StatelessWidget {
  const StarRating({
    super.key,
    required this.rating,
    this.size = 16,
    this.color = AppColors.mutedGold,
    this.showText = false,
    this.maxStars = 5,
  });

  final double rating;
  final double size;
  final Color color;
  final bool showText;
  final int maxStars;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        ...List.generate(maxStars, (i) {
          final starValue = i + 1;
          if (rating >= starValue) {
            return Icon(Icons.star_rounded, size: size, color: color);
          } else if (rating >= starValue - 0.5) {
            return Icon(Icons.star_half_rounded, size: size, color: color);
          } else {
            return Icon(Icons.star_outline_rounded, size: size, color: color.withValues(alpha: 0.3));
          }
        }),
        if (showText) ...[
          const SizedBox(width: 4),
          Text(rating.toStringAsFixed(1), style: TextStyle(fontSize: size - 4, color: color, fontWeight: FontWeight.w600)),
        ],
      ],
    );
  }
}

class BrewRatingPicker extends StatelessWidget {
  const BrewRatingPicker({
    super.key,
    required this.rating,
    required this.onRatingChanged,
    this.size = 36,
    this.color = AppColors.mutedGold,
  });

  final double rating;
  final void Function(double) onRatingChanged;
  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: List.generate(5, (i) {
        final starValue = i + 1.0;
        final isSelected = rating >= starValue;
        return GestureDetector(
          onTap: () => onRatingChanged(starValue),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 3),
            child: Icon(
              isSelected ? Icons.star_rounded : Icons.star_outline_rounded,
              size: size,
              color: isSelected ? color : color.withValues(alpha: 0.3),
            ),
          ),
        );
      }),
    );
  }
}

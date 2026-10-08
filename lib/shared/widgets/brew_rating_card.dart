import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';
import 'package:google_fonts/google_fonts.dart';

class BrewRatingCard extends StatelessWidget {
  final int rating;
  final String text;
  final DateTime date;

  const BrewRatingCard({
    Key? key,
    required this.rating,
    required this.text,
    required this.date,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.offWhite,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: AppColors.espressoBrown.withOpacity(0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              StarRating(rating: rating.toDouble()),
              Text(date.toString().split(' ')[0], style: GoogleFonts.dmSans(color: AppColors.mochaMedium, fontSize: 12)),
            ],
          ),
          const SizedBox(height: 12),
          Text(text, style: GoogleFonts.dmSans(color: AppColors.espressoBrown)),
        ],
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';
import 'package:google_fonts/google_fonts.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({Key? key}) : super(key: key);

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.offWhite,
        iconTheme: const IconThemeData(color: AppColors.espressoBrown),
        title: TextField(
          controller: _searchController,
          autofocus: true,
          decoration: InputDecoration(
            hintText: 'Search for a café or city...',
            border: InputBorder.none,
            hintStyle: GoogleFonts.dmSans(color: AppColors.mochaMedium),
          ),
          style: GoogleFonts.dmSans(color: AppColors.espressoBrown),
          onChanged: (val) {
            // debounced search
          },
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () => _searchController.clear(),
          )
        ],
      ),
      body: const BrewEmptyState(
        icon: '☕',
        title: 'Search for a café',
        subtitle: 'Find your next favorite spot.',
      ),
    );
  }
}

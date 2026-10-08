import os

files = {
    "lib/features/favorites/data/favorites_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class FavoritesRepository {
  Future<List<FavoriteEntry>> getFavorites() async => [];
  Future<FavoriteEntry> addFavorite(String placeId) async => throw UnimplementedError();
  Future<void> removeFavorite(String id) async {}
  Future<bool> isFavorite(String placeId) async => false;
}

final favoritesRepositoryProvider = Provider((ref) => FavoritesRepository());
final favoritesProvider = FutureProvider((ref) => ref.watch(favoritesRepositoryProvider).getFavorites());
final isFavoriteProvider = FutureProvider.family<bool, String>((ref, placeId) {
  return ref.watch(favoritesRepositoryProvider).isFavorite(placeId);
});
""",
    "lib/features/collections/presentation/collections_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';

class CollectionsScreen extends StatelessWidget {
  const CollectionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'My Collections'),
      body: const BrewEmptyState(
        icon: '📁',
        title: 'Create your first collection',
        subtitle: 'Group your favorite cafés by vibe, location, or trip.',
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        backgroundColor: AppColors.caramel,
        label: const Text('Create Collection', style: TextStyle(color: AppColors.offWhite)),
        icon: const Icon(Icons.add, color: AppColors.offWhite),
      ),
    );
  }
}
""",
    "lib/features/collections/presentation/collection_details_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class CollectionDetailsScreen extends StatelessWidget {
  final String collectionId;
  const CollectionDetailsScreen({Key? key, required this.collectionId}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'Collection Details'),
      body: const Center(child: Text('Collection cafes list here')),
    );
  }
}
""",
    "lib/features/collections/data/collections_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class CollectionsRepository {
  Future<List<CafeCollection>> getCollections() async => [];
  Future<CafeCollection> createCollection(String name, [String? description]) async => throw UnimplementedError();
}

final collectionsRepositoryProvider = Provider((ref) => CollectionsRepository());
""",
    "lib/features/profile/presentation/profile_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async => await Future.delayed(const Duration(seconds: 1)),
          color: AppColors.caramel,
          child: ListView(
            padding: const EdgeInsets.all(24.0),
            children: [
              Row(
                children: [
                  CircleAvatar(
                    radius: 40,
                    backgroundColor: AppColors.caramel.withOpacity(0.2),
                    child: Text('AA', style: GoogleFonts.playfairDisplay(fontSize: 32, color: AppColors.caramel)),
                  ),
                  const SizedBox(width: 16),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Alizay Aman', style: GoogleFonts.playfairDisplay(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
                      Text('@alizay', style: GoogleFonts.dmSans(color: AppColors.mochaMedium)),
                    ],
                  )
                ],
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildStat('12', 'Cafés'),
                  _buildStat('3', 'Cities'),
                  _buildStat('8', 'Favorites'),
                ],
              ),
              const SizedBox(height: 32),
              _buildListTile(context, Icons.book, 'My Journal', '/journal'),
              _buildListTile(context, Icons.favorite, 'Favorites', '/favorites'),
              _buildListTile(context, Icons.collections, 'Collections', '/collections'),
              _buildListTile(context, Icons.map, 'My Café Map', '/map/personal'),
              _buildListTile(context, Icons.tune, 'My Vibes', '/settings/preferences'),
              _buildListTile(context, Icons.edit, 'Edit Profile', '/profile/edit'),
              _buildListTile(context, Icons.settings, 'Settings', '/settings'),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStat(String value, String label) {
    return Column(
      children: [
        Text(value, style: GoogleFonts.playfairDisplay(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
        Text(label, style: GoogleFonts.dmSans(color: AppColors.mochaMedium)),
      ],
    );
  }

  Widget _buildListTile(BuildContext context, IconData icon, String title, String route) {
    return ListTile(
      leading: Icon(icon, color: AppColors.caramel),
      title: Text(title, style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.espressoBrown)),
      trailing: const Icon(Icons.chevron_right, color: AppColors.divider),
      onTap: () => context.push(route),
      contentPadding: EdgeInsets.zero,
    );
  }
}
""",
    "lib/features/profile/presentation/edit_profile_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';

class EditProfileScreen extends StatelessWidget {
  const EditProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'Edit Profile'),
      body: ListView(
        padding: const EdgeInsets.all(24.0),
        children: [
          BrewTextField(controller: TextEditingController(text: 'Alizay Aman'), label: 'Name', hint: ''),
          const SizedBox(height: 16),
          BrewTextField(controller: TextEditingController(text: 'alizay'), label: 'Username', hint: ''),
          const SizedBox(height: 16),
          BrewTextField(controller: TextEditingController(), label: 'Bio', hint: 'Write a little about yourself...', maxLines: 3),
          const SizedBox(height: 32),
          BrewButton(text: 'Save Changes', onPressed: () {}),
        ],
      ),
    );
  }
}
""",
    "lib/features/settings/presentation/settings_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: const BrewAppBar(title: 'Settings'),
      body: ListView(
        children: [
          _buildSection('Account'),
          ListTile(title: Text('Edit Profile', style: GoogleFonts.dmSans())),
          ListTile(title: Text('Change Password', style: GoogleFonts.dmSans())),
          _buildSection('App'),
          ListTile(title: Text('Location Permissions', style: GoogleFonts.dmSans())),
          ListTile(title: Text('Notification Preferences', style: GoogleFonts.dmSans())),
          _buildSection('Privacy'),
          ListTile(title: Text('Privacy Settings', style: GoogleFonts.dmSans())),
          const Divider(),
          ListTile(
            title: Text('Delete Account', style: GoogleFonts.dmSans(color: AppColors.terracotta)),
            onTap: () {},
          ),
          ListTile(
            title: Text('Sign Out', style: GoogleFonts.dmSans()),
            onTap: () {},
          ),
        ],
      ),
    );
  }

  Widget _buildSection(String title) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Text(title, style: GoogleFonts.playfairDisplay(fontSize: 18, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
    );
  }
}
""",
    "lib/features/settings/presentation/preferences_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class PreferencesScreen extends StatelessWidget {
  const PreferencesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'My Vibes'),
      body: Center(child: Text('Vibe preferences grid here')),
    );
  }
}
""",
    "lib/features/settings/presentation/privacy_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class PrivacyScreen extends StatelessWidget {
  const PrivacyScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'Privacy Settings'),
      body: Center(child: Text('Privacy settings content')),
    );
  }
}
""",
    "lib/features/settings/presentation/about_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'About Brewdrift'),
      body: Center(child: Text('Version 1.0.0')),
    );
  }
}
""",
    "lib/shared/widgets/brew_rating_card.dart": """import 'package:flutter/material.dart';
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
""",
    "lib/shared/widgets/section_header.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';

class SectionHeader extends StatelessWidget {
  final String title;
  final String? subtitle;
  final Widget? action;

  const SectionHeader({
    Key? key,
    required this.title,
    this.subtitle,
    this.action,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: GoogleFonts.playfairDisplay(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                color: AppColors.espressoBrown,
              ),
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 4),
              Text(subtitle!, style: GoogleFonts.dmSans(color: AppColors.mochaMedium)),
            ],
          ],
        ),
        if (action != null) action!,
      ],
    );
  }
}
""",
    "lib/core/utils/validators.dart": """class Validators {
  static String? validateEmail(String? value) {
    if (value == null || value.isEmpty) return 'Email is required';
    if (!RegExp(r"^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]+").hasMatch(value)) {
      return 'Please enter a valid email';
    }
    return null;
  }

  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) return 'Password is required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    return null;
  }

  static String? validateUsername(String? value) {
    if (value == null || value.isEmpty) return 'Username is required';
    if (value.length < 3) return 'Username must be at least 3 characters';
    return null;
  }

  static String? validateRequired(String? value, String fieldName) {
    if (value == null || value.trim().isEmpty) return '\$fieldName is required';
    return null;
  }

  static String? validateConfirmPassword(String? value, String original) {
    if (value != original) return 'Passwords do not match';
    return null;
  }
}
""",
    "lib/core/utils/date_utils.dart": """class DateUtilsBrew {
  static String formatVisitDate(DateTime date) {
    return '\${date.day} \${_monthName(date.month)} \${date.year}';
  }

  static String formatRelativeDate(DateTime date) {
    final now = DateTime.now();
    final diff = now.difference(date);
    if (diff.inDays == 0) return 'Today';
    if (diff.inDays == 1) return 'Yesterday';
    return '\${diff.inDays} days ago';
  }

  static String greeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  }

  static String _monthName(int month) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months[month - 1];
  }
}
""",
    "lib/shared/services/places_service.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class PlacesService {
  Future<List<Place>> searchNearby(double lat, double lng, double radiusM, dynamic filters) async => [];
  Future<List<Place>> searchByText(String query, [double? lat, double? lng]) async => [];
  Future<Place?> getPlaceDetails(String placeId) async => null;
  Future<List<PlaceRecommendation>> getRecommendations(double lat, double lng, List<String> vibes, String moodText, dynamic filters) async => [];
}

final placesServiceProvider = Provider((ref) => PlacesService());
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 3 created")

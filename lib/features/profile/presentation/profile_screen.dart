import 'package:flutter/material.dart';
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

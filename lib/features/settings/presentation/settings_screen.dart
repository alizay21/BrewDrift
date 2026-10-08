import 'package:flutter/material.dart';
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

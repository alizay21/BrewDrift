import 'package:flutter/material.dart';
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

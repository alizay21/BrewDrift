import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class EditExperienceScreen extends StatelessWidget {
  final String visitId;

  const EditExperienceScreen({super.key, required this.visitId});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'Edit Experience'),
      body: Center(child: Text('Edit form here')),
    );
  }
}

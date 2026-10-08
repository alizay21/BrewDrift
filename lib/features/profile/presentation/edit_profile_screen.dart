import 'package:flutter/material.dart';
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

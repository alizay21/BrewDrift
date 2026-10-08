import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';

class FavoritesScreen extends StatelessWidget {
  const FavoritesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: '❤️ Saved Cafés'),
      body: BrewEmptyState(
        icon: '❤️',
        title: 'No saved cafés yet',
        subtitle: 'Tap ❤️ on any café to save it.',
      ),
    );
  }
}

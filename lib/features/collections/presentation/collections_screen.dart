import 'package:flutter/material.dart';
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

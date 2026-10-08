import 'package:flutter/material.dart';
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

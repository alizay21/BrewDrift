import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class CollectionsRepository {
  Future<List<CafeCollection>> getCollections() async => [];
  Future<CafeCollection> createCollection(String name, [String? description]) async => throw UnimplementedError();
}

final collectionsRepositoryProvider = Provider((ref) => CollectionsRepository());

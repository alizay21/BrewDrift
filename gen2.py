import os

files = {
    "lib/features/home/data/home_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';
// Note: Normally we'd use ApiClient.instance, but for this mock we just return data.

class HomeRepository {
  Future<List<PlaceRecommendation>> getRecommendations(double lat, double lng, List<String> vibes, String moodText) async {
    // Mock API call
    await Future.delayed(const Duration(seconds: 1));
    return [
      PlaceRecommendation(
        place: Place(
          id: '1',
          name: 'The Cozy Corner',
          lat: lat,
          lng: lng,
          rating: 4.8,
          userRatingsTotal: 250,
          distance: 0.5,
          isOpen: true,
        ),
        vibeMatchScore: 0.95,
        matchReasons: ['Very quiet', 'Great coffee'],
      ),
    ];
  }
}

final homeRepositoryProvider = Provider<HomeRepository>((ref) {
  return HomeRepository();
});

final selectedVibesProvider = StateProvider<List<String>>((ref) => []);
final moodTextProvider = StateProvider<String>((ref) => '');

final recommendationsProvider = FutureProvider<List<PlaceRecommendation>>((ref) async {
  final repo = ref.watch(homeRepositoryProvider);
  final vibes = ref.watch(selectedVibesProvider);
  final mood = ref.watch(moodTextProvider);
  // Using dummy location for now
  return repo.getRecommendations(0, 0, vibes, mood);
});
""",
    "lib/features/discovery/presentation/explore_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:brewdrift/shared/widgets/cafe_card.dart';
import 'package:brewdrift/shared/models/models.dart';

class ExploreScreen extends StatefulWidget {
  const ExploreScreen({Key? key}) : super(key: key);

  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  bool _isMapView = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.offWhite,
        elevation: 0,
        title: GestureDetector(
          onTap: () => context.push('/search'),
          child: Container(
            height: 40,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            decoration: BoxDecoration(
              color: AppColors.warmCream,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                const Icon(Icons.search, color: AppColors.mochaMedium),
                const SizedBox(width: 8),
                Text(
                  'Search for a café...',
                  style: GoogleFonts.dmSans(color: AppColors.mochaMedium, fontSize: 14),
                ),
              ],
            ),
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(_isMapView ? Icons.list : Icons.map, color: AppColors.espressoBrown),
            onPressed: () => setState(() => _isMapView = !_isMapView),
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(48),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                _buildFilterChip('Distance'),
                _buildFilterChip('Rating'),
                _buildFilterChip('Open Now'),
                ActionChip(
                  label: const Icon(Icons.tune, size: 16, color: AppColors.espressoBrown),
                  backgroundColor: AppColors.warmCream,
                  onPressed: () => context.push('/filters'),
                ),
              ],
            ),
          ),
        ),
      ),
      body: _isMapView ? const Center(child: Text('Map View')) : _buildListView(),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        backgroundColor: AppColors.caramel,
        child: const Icon(Icons.my_location, color: AppColors.offWhite),
      ),
    );
  }

  Widget _buildFilterChip(String label) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: FilterChip(
        label: Text(label, style: GoogleFonts.dmSans(color: AppColors.espressoBrown)),
        selected: false,
        onSelected: (val) {},
        backgroundColor: AppColors.warmCream,
        selectedColor: AppColors.caramel.withOpacity(0.2),
      ),
    );
  }

  Widget _buildListView() {
    return RefreshIndicator(
      onRefresh: () async => await Future.delayed(const Duration(seconds: 1)),
      color: AppColors.caramel,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 5,
        itemBuilder: (context, index) {
          return CafeCard(
            place: Place(
              id: index.toString(),
              name: 'Discovery Cafe \${index + 1}',
              lat: 0,
              lng: 0,
              rating: 4.2 + (index * 0.1),
              userRatingsTotal: 100 + index * 10,
              distance: 1.0 + index,
              isOpen: index % 2 == 0,
            ),
          );
        },
      ),
    );
  }
}
""",
    "lib/features/discovery/data/discovery_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class DiscoveryFilters {
  final double distance;
  final double rating;
  final bool openNow;
  
  const DiscoveryFilters({
    this.distance = 5.0,
    this.rating = 0.0,
    this.openNow = false,
  });
}

class DiscoveryRepository {
  Future<List<Place>> getNearbyPlaces(double lat, double lng, double radius, DiscoveryFilters filters) async {
    await Future.delayed(const Duration(seconds: 1));
    return [];
  }

  Future<List<Place>> searchPlaces(String query, double? lat, double? lng) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return [];
  }

  Future<Place> getPlaceDetails(String placeId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return Place(id: placeId, name: 'Detail Cafe', lat: 0, lng: 0);
  }
}

final discoveryRepositoryProvider = Provider<DiscoveryRepository>((ref) => DiscoveryRepository());
final discoveryFiltersProvider = StateProvider<DiscoveryFilters>((ref) => const DiscoveryFilters());
""",
    "lib/features/discovery/presentation/search_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';
import 'package:google_fonts/google_fonts.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({Key? key}) : super(key: key);

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: AppBar(
        backgroundColor: AppColors.offWhite,
        iconTheme: const IconThemeData(color: AppColors.espressoBrown),
        title: TextField(
          controller: _searchController,
          autofocus: true,
          decoration: InputDecoration(
            hintText: 'Search for a café or city...',
            border: InputBorder.none,
            hintStyle: GoogleFonts.dmSans(color: AppColors.mochaMedium),
          ),
          style: GoogleFonts.dmSans(color: AppColors.espressoBrown),
          onChanged: (val) {
            // debounced search
          },
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () => _searchController.clear(),
          )
        ],
      ),
      body: const BrewEmptyState(
        icon: '☕',
        title: 'Search for a café',
        subtitle: 'Find your next favorite spot.',
      ),
    );
  }
}
""",
    "lib/features/discovery/presentation/filters_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';

class FiltersScreen extends StatefulWidget {
  const FiltersScreen({Key? key}) : super(key: key);

  @override
  State<FiltersScreen> createState() => _FiltersScreenState();
}

class _FiltersScreenState extends State<FiltersScreen> {
  double _distance = 5.0;
  bool _openNow = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(
        title: 'Filters',
        actions: [
          TextButton(
            onPressed: () {
              setState(() {
                _distance = 5.0;
                _openNow = false;
              });
            },
            child: Text('Reset', style: GoogleFonts.dmSans(color: AppColors.caramel)),
          )
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          Text('Distance', style: GoogleFonts.playfairDisplay(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
          Slider(
            value: _distance,
            min: 1,
            max: 20,
            divisions: 19,
            activeColor: AppColors.caramel,
            label: '\${_distance.toInt()} km',
            onChanged: (val) => setState(() => _distance = val),
          ),
          SwitchListTile(
            title: Text('Open Now', style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.espressoBrown)),
            value: _openNow,
            activeColor: AppColors.caramel,
            onChanged: (val) => setState(() => _openNow = val),
          ),
          const SizedBox(height: 32),
          BrewButton(
            text: 'Apply Filters',
            onPressed: () => context.pop(),
          )
        ],
      ),
    );
  }
}
""",
    "lib/features/map/presentation/map_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  GoogleMapController? _mapController;
  final LatLng _center = const LatLng(37.7749, -122.4194);

  void _onMapCreated(GoogleMapController controller) {
    _mapController = controller;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          GoogleMap(
            onMapCreated: _onMapCreated,
            initialCameraPosition: CameraPosition(target: _center, zoom: 14.0),
            myLocationEnabled: true,
            myLocationButtonEnabled: false,
            zoomControlsEnabled: false,
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: BrewTextField(
                controller: TextEditingController(),
                label: '',
                hint: 'Search area...',
                prefixIcon: const Icon(Icons.search, color: AppColors.mochaMedium),
              ),
            ),
          ),
          Positioned(
            bottom: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {},
              backgroundColor: AppColors.caramel,
              child: const Icon(Icons.my_location, color: AppColors.offWhite),
            ),
          ),
        ],
      ),
    );
  }
}
""",
    "lib/features/map/presentation/personal_map_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class PersonalMapScreen extends StatefulWidget {
  const PersonalMapScreen({Key? key}) : super(key: key);

  @override
  State<PersonalMapScreen> createState() => _PersonalMapScreenState();
}

class _PersonalMapScreenState extends State<PersonalMapScreen> {
  GoogleMapController? _mapController;
  final LatLng _center = const LatLng(37.7749, -122.4194);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const BrewAppBar(title: 'Your Café Trail 🗺️'),
      body: GoogleMap(
        onMapCreated: (controller) => _mapController = controller,
        initialCameraPosition: CameraPosition(target: _center, zoom: 12.0),
        myLocationEnabled: true,
        markers: {
          Marker(
            markerId: const MarkerId('1'),
            position: _center,
            icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueOrange),
          ),
        },
      ),
    );
  }
}
""",
    "lib/features/place_details/presentation/place_details_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:go_router/go_router.dart';

class PlaceDetailsScreen extends StatelessWidget {
  final Place place;
  
  const PlaceDetailsScreen({Key? key, required this.place}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 300,
            pinned: true,
            backgroundColor: AppColors.offWhite,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back_ios_new_rounded, color: AppColors.espressoBrown),
              onPressed: () => context.pop(),
            ),
            flexibleSpace: FlexibleSpaceBar(
              background: CachedNetworkImage(
                imageUrl: place.photoUrl ?? 'https://via.placeholder.com/600x400',
                fit: BoxFit.cover,
                errorWidget: (context, url, error) => Container(color: AppColors.warmCream),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    place.name,
                    style: GoogleFonts.playfairDisplay(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: AppColors.espressoBrown,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    place.address ?? 'Address not available',
                    style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.mochaMedium),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildActionButton(Icons.directions, 'Directions'),
                      _buildActionButton(Icons.favorite_border, 'Save'),
                      _buildActionButton(Icons.check_circle_outline, 'Visited'),
                      _buildActionButton(Icons.edit_outlined, 'Review'),
                    ],
                  ),
                  const SizedBox(height: 32),
                  Text('Vibe Match', style: GoogleFonts.playfairDisplay(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
                  const SizedBox(height: 16),
                  Text('Highly likely to be quiet and cozy.', style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.mochaMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(IconData icon, String label) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.warmCream,
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: AppColors.caramel),
        ),
        const SizedBox(height: 8),
        Text(label, style: GoogleFonts.dmSans(fontSize: 12, color: AppColors.espressoBrown)),
      ],
    );
  }
}
""",
    "lib/features/place_details/data/place_details_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class PlaceDetailsRepository {
  Future<Place> getPlaceDetails(String placeId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return Place(id: placeId, name: 'Detail Cafe', lat: 0, lng: 0);
  }

  Future<bool> getFavoriteStatus(String placeId) async => false;
  Future<void> addFavorite(String placeId) async {}
  Future<void> removeFavorite(String placeId) async {}
}

final placeDetailsRepositoryProvider = Provider((ref) => PlaceDetailsRepository());
""",
    "lib/features/journal/presentation/journal_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/empty_state.dart';

class JournalScreen extends StatelessWidget {
  const JournalScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'My Café Journal 📖', showBack: false),
      body: BrewEmptyState(
        icon: '📖',
        title: 'Your journal is empty',
        subtitle: 'Start exploring to save your experiences.',
      ),
    );
  }
}
""",
    "lib/features/journal/presentation/journal_entry_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:brewdrift/shared/models/models.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';

class JournalEntryScreen extends StatelessWidget {
  final VisitEntry visit;
  const JournalEntryScreen({Key? key, required this.visit}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(
        title: visit.placeName,
        actions: [
          IconButton(icon: const Icon(Icons.edit, color: AppColors.espressoBrown), onPressed: (){}),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Visited on \${visit.visitedAt.toLocal().toString().split(' ')[0]}', style: GoogleFonts.dmSans(color: AppColors.mochaMedium)),
            const SizedBox(height: 16),
            if (visit.review != null) ...[
              StarRating(rating: visit.review!.rating.toDouble(), size: 24, showText: true),
              const SizedBox(height: 16),
              Text(visit.review!.text, style: GoogleFonts.dmSans(fontSize: 16, color: AppColors.espressoBrown)),
            ]
          ],
        ),
      ),
    );
  }
}
""",
    "lib/features/journal/presentation/add_experience_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';
import 'package:brewdrift/shared/widgets/brew_button.dart';
import 'package:brewdrift/shared/widgets/brew_text_field.dart';
import 'package:brewdrift/shared/widgets/star_rating.dart';
import 'package:google_fonts/google_fonts.dart';

class AddExperienceScreen extends StatefulWidget {
  final String placeName;
  const AddExperienceScreen({Key? key, required this.placeName}) : super(key: key);

  @override
  State<AddExperienceScreen> createState() => _AddExperienceScreenState();
}

class _AddExperienceScreenState extends State<AddExperienceScreen> {
  final _experienceController = TextEditingController();
  int _rating = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: widget.placeName),
      body: ListView(
        padding: const EdgeInsets.all(24.0),
        children: [
          Text('How was it?', style: GoogleFonts.playfairDisplay(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.espressoBrown)),
          const SizedBox(height: 16),
          BrewRatingPicker(
            onRatingChanged: (val) => setState(() => _rating = val),
          ),
          const SizedBox(height: 32),
          BrewTextField(
            controller: _experienceController,
            label: 'Experience',
            hint: 'Tell your story...',
            maxLines: 5,
          ),
          const SizedBox(height: 32),
          BrewButton(text: 'Save Experience', onPressed: () {}),
        ],
      ),
    );
  }
}
""",
    "lib/features/journal/presentation/edit_experience_screen.dart": """import 'package:flutter/material.dart';
import 'package:brewdrift/core/theme/theme.dart';
import 'package:brewdrift/shared/widgets/brew_app_bar.dart';

class EditExperienceScreen extends StatelessWidget {
  const EditExperienceScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: AppColors.softBeige,
      appBar: BrewAppBar(title: 'Edit Experience'),
      body: Center(child: Text('Edit form here')),
    );
  }
}
""",
    "lib/features/journal/data/journal_repository.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:brewdrift/shared/models/models.dart';

class JournalRepository {
  Future<List<VisitEntry>> getVisits() async {
    return [];
  }
}

final journalRepositoryProvider = Provider((ref) => JournalRepository());
final visitsProvider = FutureProvider((ref) => ref.watch(journalRepositoryProvider).getVisits());
""",
    "lib/features/favorites/presentation/favorites_screen.dart": """import 'package:flutter/material.dart';
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
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Batch 2 created")

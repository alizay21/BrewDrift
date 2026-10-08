import 'package:flutter/material.dart';
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

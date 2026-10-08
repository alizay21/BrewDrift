import 'package:flutter/material.dart';
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

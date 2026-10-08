import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:brewdrift/app.dart';

void main() {
  testWidgets('BrewdriftApp smoke test', (WidgetTester tester) async {
    await dotenv.load(fileName: '.env');
    await tester.pumpWidget(
      const ProviderScope(child: BrewdriftApp()),
    );
    // Should build without errors
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}

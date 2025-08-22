// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:store_app/main.dart';

void main() {
testWidgets('Login page displays correctly', (WidgetTester tester) async {
  await tester.pumpWidget(MyApp());

  // عدّل النص ليتطابق مع زر الدخول في تطبيقك
  expect(find.text('دخول'), findsOneWidget);

  // عدّل عدد حقول النص إذا أكثر أو أقل
  expect(find.byType(TextField), findsNWidgets(2));
});

}


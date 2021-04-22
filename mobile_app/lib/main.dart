import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/app/home_page.dart';
import 'package:mobile_app/locator.dart';
import 'app/theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  setupLocator();
  await Firebase.initializeApp();

  runApp(MaterialApp(
    theme: theme(),
    home: HomePage(),
    debugShowCheckedModeBanner: false,
  ));
}

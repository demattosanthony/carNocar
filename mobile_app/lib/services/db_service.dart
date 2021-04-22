import 'package:cloud_firestore/cloud_firestore.dart';

class DbService {
  Stream getSpacesStatus() {
    return FirebaseFirestore.instance
        .collection('couch_parking_spots')
        .orderBy('status')
        .snapshots();
  }
}

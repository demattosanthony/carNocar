import 'package:apple_maps_flutter/apple_maps_flutter.dart';
import 'package:flutter/material.dart';

class CustomMap extends StatefulWidget {
  var numOpen;

  CustomMap(this.numOpen);

  @override
  _CustomMapState createState() => _CustomMapState();
}

class _CustomMapState extends State<CustomMap> {
  AppleMapController mapController;
  BitmapDescriptor _markerIconOpen;
  BitmapDescriptor _markerIconTaken;

  var _annotations = Set<Annotation>();

  void _onMapCreated(AppleMapController controller) {
    mapController = controller;

    setState(() {
      _annotations.add(Annotation(
          annotationId: AnnotationId('1'),
          position: LatLng(35.969668, -79.993379),
          icon: widget.numOpen > 0 ? _markerIconOpen : _markerIconTaken));
    });
  }

  @override
  void initState() {
    _setMarkerIcon();
    addAnnotation();
    super.initState();
  }

  void addAnnotation() async {}

  void _setMarkerIcon() async {
    _markerIconOpen = await BitmapDescriptor.fromAssetImage(
        ImageConfiguration(devicePixelRatio: 2.5), 'assets/images/pkHere.png');
    _markerIconTaken = await BitmapDescriptor.fromAssetImage(
        ImageConfiguration(devicePixelRatio: 2.5, size: Size(150, 150)),
        'assets/images/noParking.png');
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * .28,
      width: double.infinity,
      padding: EdgeInsets.only(left: 10, right: 10, bottom: 10, top: 10),
      child: ClipRRect(
        borderRadius: BorderRadius.all(Radius.circular(25.0)),
        child: Card(
          elevation: 10,
          child: AppleMap(
              onMapCreated: _onMapCreated,
              mapType: MapType.satellite,
              annotations: _annotations,
              initialCameraPosition: CameraPosition(
                  target: LatLng(35.969665, -79.993400), zoom: 16.5)),
        ),
      ),
    );
  }
}

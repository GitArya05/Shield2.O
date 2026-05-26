import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong2.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  // Center coordinates pointing near your localized testing region (Nagpur area)
  final LatLng _initialCenter = const LatLng(21.1458, 79.0882); 
  final MapController _mapController = MapController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // The open-source tile layer rendering engine
          FlutterMap(
            mapController: _mapController,
            options: MapOptions(
              initialCenter: _initialCenter,
              initialZoom: 13.0,
              maxZoom: 18.0,
              minZoom: 3.0,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.shield.client',
              ),
              // Marker and Polyline layers will go here when we wire up the routes
            ],
          ),
          
          // Minimalist Navigation Overlay
          Positioned(
            top: 50,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 15),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(8),
                boxShadow: const [
                  BoxShadow(color: Colors.black26, blurRadius: 10, offset: Offset(0, 2))
                ],
              ),
              child: const TextField(
                decoration: InputDecoration(
                  hintText: 'Enter destination...',
                  border: InputBorder.none,
                  icon: Icon(Icons.search, color: Colors.black87),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
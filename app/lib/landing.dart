import 'package:app/search_engine/search_engine_ui.dart';
import 'package:flutter/material.dart';

class Landing extends StatefulWidget {
  const Landing({Key? key}) : super(key: key);

  @override
  State<Landing> createState() => _LandingState();
}

class _LandingState extends State<Landing> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      // decoration: const BoxDecoration(
      //   gradient: LinearGradient(
      //     colors: [
      //       Colors.deepOrange,
      //       Colors.deepOrangeAccent,
      //     ],
      //     begin: Alignment.topLeft,
      //     end: Alignment.bottomLeft,
      //   ),
      // ),
      child: Scaffold(
        appBar: AppBar(
          elevation: 0,
          backgroundColor: Colors.transparent,
        ),
        backgroundColor: Colors.transparent,
        body: SingleChildScrollView(
          child: Container(
            padding: const EdgeInsets.all(8.0),
            margin: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  "Reddit and Google Trends Analysis Engine",
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.headline3,
                ),
                const Padding(padding: EdgeInsets.all(8.0)),
                const SearchEngineUi(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

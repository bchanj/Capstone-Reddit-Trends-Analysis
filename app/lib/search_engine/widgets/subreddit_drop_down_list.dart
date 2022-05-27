import 'dart:html';

import 'package:app/search_engine/bloc/search_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SubredditDropDownList extends StatefulWidget {
  const SubredditDropDownList({Key? key}) : super(key: key);
  @override
  State<SubredditDropDownList> createState() => _SubredditDropDownListState();
}

class _SubredditDropDownListState extends State<SubredditDropDownList> {
  late String _value;
  final List<String> _dropDownValues = <String>[
    "r/GameDeals",
  ];

  @override
  void initState() {
    super.initState();
    _value = _dropDownValues.first;
  }

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      items: List.generate(
        _dropDownValues.length,
        (index) => DropdownMenuItem(
          child: Text(_dropDownValues[index]),
          value: _dropDownValues[index],
        ),
      ),
      value: _value,
      onChanged: (String? value) {
        if (value == null) return;
        setState(() {
          _value = value;
        });
        BlocProvider.of<SearchBloc>(context).add(
          Search(
            subreddit: value,
          ),
        );
      },
    );
  }
}

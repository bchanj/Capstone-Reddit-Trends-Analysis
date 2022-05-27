import 'package:app/search_engine/bloc/search_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class DealTitleSearchField extends StatefulWidget {
  const DealTitleSearchField({Key? key}) : super(key: key);

  @override
  State<DealTitleSearchField> createState() => _DealTitleSearchFieldState();
}

class _DealTitleSearchFieldState extends State<DealTitleSearchField> {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: TextFormField(
        decoration: InputDecoration(
          labelText: "Deal Title",
          filled: true,
          prefixIcon: const Icon(Icons.search),
          suffixIcon: IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () {
              _controller.clear();
            },
          ),
        ),
        controller: _controller,
        onChanged: (String? value) {
          String? searchValue;
          if (value?.isEmpty ?? true) {
            searchValue = null;
          } else {
            searchValue = value;
          }
          BlocProvider.of<SearchBloc>(context).add(
            Search(
              title: searchValue,
            ),
          );
        },
      ),
    );
  }
}

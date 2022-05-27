import 'package:app/search_engine/bloc/search_bloc.dart';
import 'package:app/search_engine/widgets/widgets.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SearchEngineUi extends StatefulWidget {
  const SearchEngineUi({Key? key}) : super(key: key);

  @override
  State<SearchEngineUi> createState() => _SearchEngineUiState();
}

class _SearchEngineUiState extends State<SearchEngineUi> {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) {
        final bloc = SearchBloc();
        bloc.add(const Search());
        return bloc;
      },
      child: Column(
        children: const [
          SearchBar(),
          SearchBody(),
        ],
      ),
    );
  }
}

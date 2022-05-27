part of 'search_bloc.dart';

@immutable
abstract class SearchState {
  const SearchState();
}

class SearchInitial extends SearchState {}

class SearchLoading extends SearchState {}

class SearchFailure extends SearchState {
  final String error;
  const SearchFailure({required this.error});
}

class SearchSuccess extends SearchState {
  final List<Deal> deals;
  const SearchSuccess({required this.deals});
}

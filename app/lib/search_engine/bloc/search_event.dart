part of 'search_bloc.dart';

@immutable
abstract class SearchEvent {
  const SearchEvent();
}

class Search extends SearchEvent {
  final String? title;
  final String? price;
  final String? subreddit;
  const Search({
    this.title,
    this.price,
    this.subreddit,
  });
}

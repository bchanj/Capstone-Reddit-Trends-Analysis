import 'package:app/models/deal.dart';
import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';
import 'package:dio/dio.dart';
import 'dart:convert' as convert;

part 'search_event.dart';
part 'search_state.dart';

class SearchBloc extends Bloc<SearchEvent, SearchState> {
  final String endpoint =
      'https://reddit-and-google-analysis.azurewebsites.net/api/trends-service';

  final Uri base = Uri(
      scheme: "https",
      host: "reddit-and-google-analysis.azurewebsites.net",
      path: "/api/trends-service");

  final Dio client = Dio();

  SearchBloc() : super(SearchInitial()) {
    on<Search>(_searchHandler);
  }

  Future<void> _searchHandler(Search event, Emitter<SearchState> emit) async {
    emit(SearchLoading());

    try {
      final Uri target = Uri(
        scheme: base.scheme,
        host: base.host,
        path: base.path,
        queryParameters: {
          if (event.price != null) ...{"price": event.price},
          if (event.title != null) ...{"title": event.title},
          if (event.subreddit != null) ...{"discount": event.subreddit},
        },
      );

      print(target.queryParameters);

      Response res = await client.getUri(
        target,
        options: Options(
          responseType: ResponseType.plain,
        ),
      );

      List<Deal> deals = (convert.jsonDecode(res.data) as List<dynamic>)
          .map((json) => Deal.fromJson(json))
          .toList();

      emit(SearchSuccess(deals: deals));
    } catch (e) {
      emit(SearchFailure(error: e.toString()));
    }
  }
}

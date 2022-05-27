import 'package:app/models/deal.dart';
import 'package:app/search_engine/bloc/search_bloc.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:url_launcher/url_launcher_string.dart';

class SearchBody extends StatefulWidget {
  const SearchBody({Key? key}) : super(key: key);

  @override
  State<SearchBody> createState() => _SearchBodyState();
}

class _SearchBodyState extends State<SearchBody> {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<SearchBloc, SearchState>(
      builder: (context, state) {
        if (state is SearchLoading || state is SearchInitial) {
          return LinearProgressIndicator(
            color: Theme.of(context).colorScheme.primary,
          );
        }
        if (state is SearchFailure) {
          return Container(
            padding: const EdgeInsets.only(bottom: 4),
            margin: const EdgeInsets.only(top: 4),
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(4),
                bottomRight: Radius.circular(4),
              ),
            ),
            child: ListTile(
              tileColor: Colors.white,
              title: const Text("Failed to load results"),
              subtitle: Text(state.error),
            ),
          );
        }
        if (state is SearchSuccess) {
          if (state.deals.isEmpty) {
            return Container(
              padding: const EdgeInsets.only(bottom: 4),
              margin: const EdgeInsets.only(top: 4),
              decoration: const BoxDecoration(
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(4),
                  bottomRight: Radius.circular(4),
                ),
              ),
              child: ListTile(
                tileColor: Colors.white,
                leading: const Icon(CupertinoIcons.clear_circled),
                title: const Text("No Results"),
              ),
            );
          }
          return Container(
            margin: const EdgeInsets.only(top: 4),
            padding: const EdgeInsets.only(bottom: 4),
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(4),
                bottomRight: Radius.circular(4),
              ),
            ),
            child: ListView.builder(
              shrinkWrap: true,
              itemCount: state.deals.length,
              itemBuilder: (context, index) {
                final Deal deal = state.deals[index];
                return ListTile(
                  tileColor: Colors.white,
                  title: Text(deal.title ?? ""),
                  subtitle: Text(deal.price ?? ""),
                  leading: Text(deal.discount ?? ""),
                  trailing: const Icon(Icons.chevron_right_rounded),
                  onTap: () async {
                    if (deal.url != null &&
                        await canLaunchUrlString(deal.url!)) {
                      launchUrlString(deal.url!);
                    } else {
                      showDialog(
                        context: context,
                        builder: (BuildContext context) {
                          return AlertDialog(
                            content: const Text(
                                "We apologize, but we were unable to open that url. Please try again later"),
                            actions: [
                              TextButton.icon(
                                  onPressed: () => Navigator.of(context).pop,
                                  icon: const Icon(
                                    Icons.clear,
                                    color: Colors.red,
                                  ),
                                  label: const Text("Close"))
                            ],
                          );
                        },
                      );
                    }
                  },
                );
              },
            ),
          );
        }
        throw UnimplementedError();
      },
    );
  }
}

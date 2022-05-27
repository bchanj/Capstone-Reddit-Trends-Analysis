import 'package:app/search_engine/widgets/widgets.dart';
import 'package:flutter/material.dart';

class SearchBar extends StatelessWidget {
  const SearchBar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(4),
          topRight: Radius.circular(4),
        ),
        color: Colors.transparent,
      ),
      child: Row(
        children: const [
          // SubredditDropDownList(),
          DealTitleSearchField(),
          // DealPriceSearchField(),
        ],
      ),
    );
  }
}

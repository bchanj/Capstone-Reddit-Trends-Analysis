import 'package:json_annotation/json_annotation.dart';

part 'deal.g.dart';

@JsonSerializable()
class Deal {
  @JsonKey(name: "title")
  final String? title;
  @JsonKey(name: "discount")
  final String? discount;
  @JsonKey(name: "price")
  final String? price;
  @JsonKey(name: "url")
  final String? url;

  const Deal({
    this.title,
    this.price,
    this.discount,
    this.url,
  });

  factory Deal.fromJson(Map<String, dynamic> json) => _$DealFromJson(json);

  Map<String, dynamic> toJson() => _$DealToJson(this);
}

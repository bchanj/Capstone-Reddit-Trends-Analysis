// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'deal.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Deal _$DealFromJson(Map<String, dynamic> json) => Deal(
      title: json['title'] as String?,
      price: json['price'] as String?,
      discount: json['discount'] as String?,
      url: json['url'] as String?,
    );

Map<String, dynamic> _$DealToJson(Deal instance) => <String, dynamic>{
      'title': instance.title,
      'discount': instance.discount,
      'price': instance.price,
      'url': instance.url,
    };

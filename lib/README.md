https://yandex.ru/dev/taxi/doc/dg/concepts/trip-info-docpage/#trip-info

Поддерживаются форматы ответа JSON и protobuf. Для выбора формата ответа передайте необязательный заголовок Accept:


Accept: application/json — ответ в формате JSON. Значение по умолчанию.
Accept: application/x-protobuf — ответ в формате protobuf.

Ответ в формате protobuf
Если запрос был отправлен с заголовком Accept: application/x-protobuf ответом будет являться сообщение TaxiInfo.

Для декодирования protobuf-ответа используйте следующее описание протокола:

```
message TaxiOption
{
  required double price = 1;
  required double min_price = 2;
  optional double waiting_time = 3;
  required string class_name = 4;
  required string class_text = 5;
  required int32 class_level = 6;
  required string price_text = 7;
}

message TaxiInfo
{
  repeated TaxiOption options = 1;
  required string currency = 2;
  optional double distance = 3;
  optional double time = 4;
}
```

# Синтаксис запроса

GET  https://taxi-routeinfo.taxi.yandex.net/taxi_info?clid=<clid>&apikey=<apikey>&rll=<lon,lat~lon,lat>&class=<class_str>&req=<req_str>


Пример запроса для нескольких тарифов

В запросе указаны тарифы «Эконом» и «Бизнес» и не указана точка назначения:

```
Пример запроса для одного тарифа
GET https://taxi-routeinfo.taxi.yandex.net/taxi_info?rll=37.589569560,55.733780~37,56&clid=t...3&apikey=q...3

Пример запроса для нескольких тарифов
В запросе указаны тарифы «Эконом» и «Бизнес» и не указана точка назначения:

GET https://taxi-routeinfo.taxi.yandex.net/taxi_info?rll=37.589569560,55.733780~37,56&clid=t...3&apikey=q...3
GET https://taxi-routeinfo.taxi.yandex.net/taxi_info?rll=37.589569560,55.733780&clid=t...3&apikey=q...3&class=econom,vip&req=check,yellowcarnumber
```
Возможные коды ответа
Ответ на данный запрос может содержать следующие коды ответа:

200 — запрос выполнен успешно.
204 — запрашиваемый регион не поддерживается сервисом.
400 — параметры запроса были не указаны или указаны некорректно.
403 — ошибка авторизации. Были указаны некорректные значения ключа API или идентификатора клиента.
500 — внутренняя ошибка сервера.
В случае ошибок с кодами 400 и 403 в теле ответа будет содержаться текст сообщения об ошибке.
# serialization-benchmark

## tl;dr
```
# clone the repo, cd into it
docker-compose up
```
поднимет прокси на `localhost:2000`.

Поддерживаемые команды:
```
get_result all
get_result <format>
Available formats:
Pickle, JSON, XML, YAML, MessagePack, Avro, ProtoBuf
```
где в качестве `format` можно указать любой из:
```
Pickle, JSON, XML, YAML, MessagePack, Avro, ProtoBuf
```

Пример работы:
```
❯ nc -u localhost 2000
get_result JSON
JSON - 13150 - 33ms - 22ms
get_result ProtoBuf
ProtoBuf - 10641 - 3ms - 6ms
get_result all
ProtoBuf - 10641 - 4ms - 6ms
Pickle - 3752 - 7ms - 7ms
MessagePack - 9906 - 8ms - 13ms
JSON - 13150 - 36ms - 23ms
Avro - 8863 - 36ms - 48ms
XML - 27491 - 382ms - 381ms
YAML - 14218 - 604ms - 650ms
get_result blabla
Invalid request, available options are:
get_result all
get_result <format>
Available formats:
Pickle, JSON, XML, YAML, MessagePack, Avro, ProtoBuf
```

## Описание проекта
В папке `bench` лежит код, отвечающий за прогон бенчмарков,
и соответствующий `Dockerfile`. Он общий для всех форматов, с каким
конкретно форматом запустится контейнер определяется через переменную
окружения `SER_FORMAT`.

Приложение запускает два процесса (т. к. не хотелось возиться с
мультиплексированием + GIL), один из них принимает юникаст траффик на своем
индивидуальном адресе, другой принимает мультикаст сообщения на
общем для бенч контейнеров мультикаст адресе `228.69.42.0:7777`.

В `bench/sample_data` лежит код, генерирующий тестовые данные.
Они представляют из себя словарь, описывающий структуру некоего
учебного заведения: несколько групп, в каждой из которой есть
определенное кол-во студентов, у них есть оценки по дисциплинам
и еще немного другой информации. Структуру описал датаклассами,
поэтому смотреть по коду вероятно будет нагляднее.

Сами бенчмарки запускаются на словаре, за исключением протобуфа,
т. к. в нем свой отдельный класс. Так же для XML пришлось немного
извращаться и преобразовывать словарь, чтобы сохранять информацию
о типах в аттрибутах.

В папке `proxy` лежит код прокси (логично) и соответствующий `Dockerfile`.

Адреса контейнеров лежат в `config.json`.

Все запускается через `docker-compose`. Образы контейнеров
подтягиваются с Docker Hub.

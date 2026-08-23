# Курсовая работа по ООП (4й модуль) + дополненна курсовой работой по БД (5й модуль)
В этой работе реализована программа, которая собирает данные о самолетах в воздушных пространствах тех стран,
которые выберет пользователь.  
Чтобы получить географические координаты стран используется API `nominatim.openstreetmap.org`,
а чтобы получить информацию о самолетах — API `opensky-network.org`.

Так же реализован класс DBManager для добавления данных в БД БД PostgreSQL и работа с этими данными
## Установка:

1. Клонируйте репозиторий:
```
https://github.com/oMakom/CoursePaperOOP_DB.git
```

2. Установите зависимости:
```
pip install -r requirements.txt
poetry install
```

### Реализация класса для работы с информацией о самолетах`Aeroplane(callsign: str, country: str, velocity: float, altitude: float)`
- **Класс реализованы в модуле aircraft_data_handler.py**
- cast_to_object_list(cls, country_aeroplanes: list[dict]) - Создает из списка словарей список объектов Aeroplane
- __eq__ __gt__ __lt__ - методы сравнения по скорости и высоте
- __str__ - метод для вывода в читаемом виде
- to_dict - метод преобразования в словарь
### Реализация класса для работы с файлами`JSONSaver(self, file_path=None)`
- **Класс реализованы в модуле json_saver.py**
- obj_to_list(aeroplane_obj: list[Aeroplane] | Aeroplane) - Принимает объект, либо список объектов. Приводит в виду list[dict]
- read_data_file() - """Читает данные из файла "../data/data_aeroplanes.json", если ошибка чтения, то на выходе пустой список"""
- write_to_json(data_list: list) - Записывает данные в файл ( по умолчанию "../data/data_aeroplanes.json") 
- add_aeroplane(aeroplane: list[Aeroplane] | Aeroplane) - метод для сохранения/добавления информации о самолетах в JSON-файл
- delete_aeroplane(self, callsign: str) - метод удаляет данные из файла по позывному
### Реализация класса для работы Api ApiCountryCoordinates() и ApiAeroplanesCountry()`
- **Классы реализованы в модуле api_connector.py**
- fetch_data - метод получения данных из API
### Реализация класса для работы БД PostgreSQL`
- **Класс реализованы в модуле database.py**
- _create_table - Создание двух таблиц countries и aeroplanes
- close - Метод для закрытия соединений с базой данных
- refresh_tables - Метод для удаления таблиц из базы данных и перезаписи новых
- insert_data - Функция обновляет данные по стране и самолетам в ее границах:
        **country** - страна;
        **db_date_country** - 'boundingbox' указанной страны;
        **db_date_aeroplanes** - список спосков данных о самолетах в границе данной страны.
- __db_date_tuple_to_dict(columns: list, rows: list[tuple]) -> list[dict] - Преобразует данные из базы дынных в 
удобочитаемый вид(список кортежей в список словарей)
- get_countries_and_aeroplanes_count -> list[dict] - получает список всех стран и количество самолетов в их
воздушных пространствах
- get_all_aeroplanes -> list[dict] - получает список всех воздушных судов
- get_avg_speed -> list[dict] - получает среднюю скорость по самолетам
- get_aeroplanes_with_higher_speed -> list[dict] - получает список всех самолетов, у которых скорость выше средней
- get_aeroplanes_with_keyword (search: str)-> list[dict] - получает список всех самолетов, в позывном которых содержатся 
переданные в метод символы

- ### Функционал интерфейса реализован в модуле interface.py
- ### Пробный вызов функционала и связующая интерфес функция вызваны в модуле main.py

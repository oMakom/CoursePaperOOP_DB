import os

from dotenv import load_dotenv

from api_connector import ApiAeroplanesCountry, ApiCountryCoordinates
from database import DBManager

"""
def user_interaction() -> None:
    while True:
        country = input("Введите название страны (пример ввода: RUSSIA): ")  # Например RUSSIA
        if country:
            break
        print("Страна не может быть пустой.")
    try:
        aeroplanes = get_aeroplanes_by_country(country)
    except Exception as e:
        print(f"Ошибка при запросе данных: {e}")
        return
    if not aeroplanes:
        print("Данные о самолетах не получены. Завершение программы")
        return

    # фильтрация по стране регистрации
    filter_words = (
        input(
            "Введите названия стран для фильтрации по стране регистрации через запятую "
            "(пример ввода: United States, Germany): "
        )
        .strip()
        .split(",")
    )

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)

    # фильтрация по диапазону высот полета
    while True:
        altitude_range = input("Введите диапазон высот полета (Пример ввода: 200 - 10200): ")
        if altitude_range:
            range_list = altitude_range.split("-")
            try:
                altitude_min = int(range_list[0])
                altitude_max = int(range_list[1])

                if altitude_min >= altitude_max:
                    print("Минимальная высота должна быть меньше максимальной")
                if altitude_min < altitude_max:
                    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
                    break

            except ValueError:
                print("Высота должна быть числом")
        else:
            print("Данные диапазона высот не введены. Фильтрация по диапазону высот пропущена")
            ranged_aeroplanes = filtered_aeroplanes
            break

    # сортировка по высоте полета по убыванию
    sorted_by_altitude = sort_aeroplanes(ranged_aeroplanes)

    # вывод топ n самолетов
    while True:
        top_n = input("Введите количество самолетов для вывода в топ N: ").strip()
        try:
            n = int(top_n)
            if n > 0:
                break
            print("Число должно быть больше 0.")
        except ValueError:
            print("Введите целое число.")

    top_n_aeroplanes = get_top_aeroplanes(sorted_by_altitude, top_n)

    # вывод результата
    print_all_aeroplanes(top_n_aeroplanes)
"""

def main_db():
    country_list = ['RUSSIA', 'United States', 'Germany', 'France', 'United Kingdom', 'Canada', 'Estonia', 'Austria', 'Sweden', 'Turkey']
    #country_list = ['United States']

    load_dotenv()

    db_config = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'dbname': os.getenv('POSTGRES_DB')
    }

    db = DBManager(**db_config)
    """
    # Код для добавления данных, можно закомментировать после добавления и заполнения таблиц
    db.refresh_tables()
    for country in country_list:
        api_county = ApiCountryCoordinates()
        geo_coord = api_county.fetch_data(country)

        api_aeroplanes = ApiAeroplanesCountry()
        aeroplanes_list = api_aeroplanes.fetch_data(geo_coord)

        db.insert_data(country, geo_coord, aeroplanes_list)
    """
    print('------------------------------#1------------------------------------')
    # список всех стран и количество самолетов в их воздушных пространствах
    print(db.get_countries_and_aeroplanes_count())
    print('------------------------------#2------------------------------------')
    # список всех воздушных судов (уникальных, так как "области" стран могут накладываться)
    print(db.get_all_aeroplanes())
    print('------------------------------#3------------------------------------')
    # средняя скорость по всем уникальным самолетам
    print(db.get_avg_speed())
    print('------------------------------#4------------------------------------')
    # список всех самолетов, у которых скорость выше средней
    print(db.get_aeroplanes_with_higher_speed())
    print('------------------------------#5------------------------------------')
    # список всех самолетов, в позывном которых содержатся переданные в метод символы
    print(db.get_aeroplanes_with_keyword('aca'))

    db.close()

if __name__ == "__main__":
    main_db()

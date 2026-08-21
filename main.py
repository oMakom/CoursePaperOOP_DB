
from database import DBManager

import os

from dotenv import load_dotenv

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
    load_dotenv()

    db_config = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'dbname': os.getenv('POSTGRES_DB')
    }

    db = DBManager(**db_config)
    db.close()

if __name__ == "__main__":
    main_db()

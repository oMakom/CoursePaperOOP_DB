import os

from dotenv import load_dotenv

from api_connector import ApiCountryCoordinates, ApiAeroplanesCountry
from database import DBManager


def main_db():
    country_list = ['RUSSIA', 'United States', 'Germany', 'France', 'United Kingdom', 'Canada', 'Estonia', 'Austria', 'Sweden', 'Turkey']

    load_dotenv()

    db_config = {
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'dbname': os.getenv('POSTGRES_DB')
    }

    db = DBManager(**db_config)
    # ВНИМАНИЕ: True ТОЛЬКО для ПЕРВОЙ загрузки данных или полного сброса.
    # Если данные уже есть, оставь False, чтобы не делать запрос API лишний раз и не терять данные.
    fill_data = False

    try:
        if fill_data:
            # Код для добавления данных
            print("--- Очистка и создание таблиц ---")
            db.refresh_tables()
            print("--- Загрузка данных из API ---")
            for country in country_list:
                api_county = ApiCountryCoordinates()
                geo_coord = api_county.fetch_data(country)

                api_aeroplanes = ApiAeroplanesCountry()
                aeroplanes_list = api_aeroplanes.fetch_data(geo_coord)

                db.insert_data(country, geo_coord, aeroplanes_list)
            print("Данные загружены (закомментировано для демонстрации).")
        print('------------------------------#1  (Страны и кол-во самолётов)------------------------------------')
        # список всех стран и количество самолетов в их воздушных пространствах
        metod_1 = db.get_countries_and_aeroplanes_count()
        print(f"Найдено записей (страны + кол-во самолётов): {len(metod_1)}")
        for item in metod_1:
            print(item)
        print('------------------------------#2 Все уникальные самолёты------------------------------------')
        # список всех воздушных судов (уникальных, так как "области" стран могут накладываться)
        metod_2 = db.get_all_aeroplanes()
        print(f"Всего уникальных самолётов: {len(metod_2)}")
        for item in metod_2[:25]:  # для проверки первые 25
            print(item)
        print('------------------------------#3 Средняя скорость (AVG)------------------------------------')
        # средняя скорость по всем уникальным самолетам
        metod_3 = db.get_avg_speed()
        print(f"Средняя скорость уникальных самолётов: {metod_3[0]["aeroplanes_avg_velocity"]:.2f}")
        print(metod_3)
        print('------------------------------#4 Самолёты выше средней------------------------------------')
        # список всех самолетов, у которых скорость выше средней
        metod_4 = db.get_aeroplanes_with_higher_speed()
        print(f"Самолётов со скоростью выше средней: {len(metod_4)}")
        for item in metod_4[:25]: # для проверки первые 25
            print(item)
        print('------------------------------#5 Поиск по ключевым словам------------------------------------')
        # список всех самолетов, в позывном которых содержатся переданные в метод символы
        metod_5 = db.get_aeroplanes_with_keyword('aca')
        print(f"Найдено самолётов с 'aca' в позывном: {len(metod_5)}")
        for item in metod_5[:25]:  # для проверки первые 25
            print(item)
    finally:
        db.close()

if __name__ == "__main__":
    main_db()

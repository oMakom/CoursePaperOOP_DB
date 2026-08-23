import os

from dotenv import load_dotenv

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

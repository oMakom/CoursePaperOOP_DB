import psycopg2
from psycopg2._psycopg import List


class DBManager:
    """ Класс для работы с БД PostgreSQL"""
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432',
                ):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def _create_table(self,table_name: str):
        """Создание двух таблиц countries и aeroplanes"""

        if table_name == 'countries':
            with self.conn:
                self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS countries (
                   country_id SERIAL PRIMARY KEY,
                   country_name VARCHAR(100),
                   la_min DOUBLE PRECISION,
                   la_max DOUBLE PRECISION,
                   lo_min DOUBLE PRECISION,
                   lo_max DOUBLE PRECISION
                   );
                   """)
        if table_name == 'aeroplanes':
            with self.conn:
                self.cur.execute("""
                   CREATE TABLE IF NOT EXISTS aeroplanes (
                   aeroplanes_id SERIAL PRIMARY KEY,
                   country_id INT REFERENCES countries(country_id),
                   callsign VARCHAR(8) NOT NULL,
                   reg_country VARCHAR(100),
                   velocity REAL,
                   altitude REAL
                   );
                   """)

    def close(self):
        """Метод для закрытия соединений с базой данный"""
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def refresh_tables(self):
        """Метод для удаляет таблиц из базы данных и перезаписи новых"""
        with self.conn:
            self.cur.execute("""DROP TABLE IF EXISTS aeroplanes""")
            self.cur.execute("""DROP TABLE IF EXISTS countries""")
        self._create_table('countries')
        self._create_table('aeroplanes')

    def insert_data(self, country: str, db_date_country: list, db_date_aeroplanes: list):
        """Функция обновляет данные по стране и самолетам в ее границах
        country - страна
        db_date_country - 'boundingbox' указанной страны
        db_date_aeroplanes - список спосков данных о самолетах в границе данной страны
        """
        with self.conn:
            self.cur.execute(
                f"INSERT INTO countries (country_name, la_min, la_max, lo_min, lo_max) VALUES (%s, %s, %s, %s, %s)  RETURNING country_id;",
                (country, db_date_country[0], db_date_country[1], db_date_country[2], db_date_country[3]))
            country_id = self.cur.fetchone()[0]
            for date in db_date_aeroplanes:
                self.cur.execute(
                    f"INSERT INTO aeroplanes (country_id, callsign, reg_country, velocity, altitude) VALUES (%s, %s, %s, %s, %s)",
                    (country_id, date[1], date[2], date[9], date[7]))

    @staticmethod
    def __db_date_tuple_to_dict(columns: list, rows: list[tuple]) -> list[dict]:
        """Преобразует данные из базы дынных в удобочитаемый вид(список кортежей в список словарей)"""
        date = []
        for row in rows:
            date.append(dict(zip(columns, row)))
        return date

    def get_countries_and_aeroplanes_count(self) -> list[dict]:
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        with self.conn:
            self.cur.execute("""SELECT country_name, COUNT(aeroplanes.callsign) AS count_aeroplanes FROM countries
                                JOIN aeroplanes USING(country_id)
                                GROUP by country_name;""")
            #получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            #получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            countries_and_aeroplanes_count = self.__db_date_tuple_to_dict(columns, rows)
            return countries_and_aeroplanes_count

    def get_all_aeroplanes(self) -> list[dict]:
        """получает список всех воздушных судов"""
        with self.conn:
            self.cur.execute("""SELECT DISTINCT ON (callsign) * FROM aeroplanes""")
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            all_aeroplanes = self.__db_date_tuple_to_dict(columns, rows)
            return all_aeroplanes

    def get_avg_speed(self) -> None:
        """получает среднюю скорость по самолетам"""
        pass
    def get_aeroplanes_with_higher_speed(self) -> None:
        """получает список всех самолетов, у которых скорость выше средней"""
        pass
    def get_aeroplanes_with_keyword(self) -> None:
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        pass
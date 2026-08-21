import psycopg2

class DBManager:
    """ Класс для работы с БД PostgreSQL"""
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432',
                ):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self._refresh_tables()
        self._create_table('countries')
        self._create_table('aeroplanes')

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

    def _refresh_tables(self):
        """Метод для удаляет таблиц из базы данных"""
        with self.conn:
            self.cur.execute("""DROP TABLE IF EXISTS aeroplanes""")
            self.cur.execute("""DROP TABLE IF EXISTS countries""")

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

    def get_countries_and_aeroplanes_count(self) -> None:
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        pass
    def get_all_aeroplanes(self) -> None:
        """получает список всех воздушных судов"""
        pass
    def get_avg_speed(self) -> None:
        """получает среднюю скорость по самолетам"""
        pass
    def get_aeroplanes_with_higher_speed(self) -> None:
        """получает список всех самолетов, у которых скорость выше средней"""
        pass
    def get_aeroplanes_with_keyword(self) -> None:
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        pass
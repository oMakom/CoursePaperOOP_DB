import psycopg2

class DBManager:
    """ Класс для работы с БД PostgreSQL"""
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432',
                ):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

        self._create_table('countries')
        self._create_table('aeroplanes')

    def _create_table(self,table_name: str):
        """Создание двух таблиц countries и aeroplanes"""
        if table_name == 'countries':
            with self.conn:
                self.cur.execute(f"""
                   CREATE TABLE IF NOT EXISTS {table_name} (
                   country_id SERIAL PRIMARY KEY,
                   country_name VARCHAR(255),
                   la_min DOUBLE PRECISION,
                   la_max DOUBLE PRECISION,
                   lo_min DOUBLE PRECISION,
                   lo_max DOUBLE PRECISION
                   );
                   """)
        if table_name == 'aeroplanes':
            with self.conn:
                self.cur.execute(f"""
                   CREATE TABLE IF NOT EXISTS {table_name} (
                   aeroplanes_id SERIAL PRIMARY KEY,
                   country_id INT REFERENCES countries(country_id),
                   callsign VARCHAR(10) UNIQUE NOT NULL,
                   velocity REAL NOT NULL,
                   altitude REAL NOT NULL
                   );
                   """)

    def close(self):
        """Метод для закрытия соединений с базой данный"""
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

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
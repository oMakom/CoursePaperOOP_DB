import psycopg2


class DBManager:
    """Класс для работы с БД PostgreSQL.
    Отвечает за создание таблиц, загрузку данных и выполнение аналитических запросов"""

    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
    ):
        """
        Инициализирует соединение с базой данных.
            :dbname: Имя базы данных.
            :user: Пользователь БД.
            :password: Пароль пользователя.
            :host: Хост БД.
            :port: Порт БД.
        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    @staticmethod
    def __db_date_tuple_to_dict(columns: list, rows: list[tuple]) -> list[dict]:
        """Преобразует данные из базы дынных в удобочитаемый вид(список кортежей в список словарей)"""
        date = []
        for row in rows:
            date.append(dict(zip(columns, row)))
        return date

    def _create_table(self, table_name: str) -> None:
        """Создание двух таблиц countries и aeroplanes"""

        if table_name == "countries":
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
        if table_name == "aeroplanes":
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

    def close(self) -> None:
        """Метод для закрытия соединений с базой данных"""
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def refresh_tables(self) -> None:
        """Метод для удаления таблиц из базы данных и перезаписи новых"""
        with self.conn:
            self.cur.execute("""DROP TABLE IF EXISTS aeroplanes CASCADE""")
            self.cur.execute("""DROP TABLE IF EXISTS countries""")
        self._create_table("countries")
        self._create_table("aeroplanes")

    def insert_data(self, country: str, db_date_country: list, db_date_aeroplanes: list) -> None:
        """Функция обновляет данные по стране и самолетам в ее границах
        country - страна
        db_date_country - 'boundingbox' указанной страны
        db_date_aeroplanes - список спосков данных о самолетах в границе данной страны
        """
        with self.conn:
            self.cur.execute(
                """INSERT INTO countries (country_name, la_min, la_max, lo_min, lo_max)
                            VALUES (%s, %s, %s, %s, %s)  RETURNING country_id;""",
                (country, db_date_country[0], db_date_country[1], db_date_country[2], db_date_country[3]),
            )
            country_id = self.cur.fetchone()[0]
            for date in db_date_aeroplanes:
                self.cur.execute(
                    """INSERT INTO aeroplanes (country_id, callsign, reg_country, velocity, altitude)
                                VALUES (%s, %s, %s, %s, %s)""",
                    (country_id, date[1], date[2], date[9], date[7]),
                )

    def get_countries_and_aeroplanes_count(self) -> list[dict]:
        """получает список всех стран и количество самолетов в их воздушных пространствах.
            :return: Список словарей [{'country_name': ..., 'count_aeroplanes': ...}]"""
        with self.conn:
            self.cur.execute("""SELECT country_name, COUNT(aeroplanes.callsign) AS count_aeroplanes FROM countries
                                JOIN aeroplanes USING(country_id)
                                GROUP by country_name;""")
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            countries_and_aeroplanes_count = self.__db_date_tuple_to_dict(columns, rows)
            return countries_and_aeroplanes_count

    def get_all_aeroplanes(self) -> list[dict]:
        """получает список всех воздушных судов"""
        with self.conn:
            self.cur.execute("""SELECT DISTINCT ON (callsign) * FROM aeroplanes;""")
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            all_aeroplanes = self.__db_date_tuple_to_dict(columns, rows)
            return all_aeroplanes

    def get_avg_speed(self) -> list[dict]:
        """получает среднюю скорость по самолетам"""
        with self.conn:
            self.cur.execute("""SELECT AVG(velocity) as aeroplanes_avg_velocity
                                FROM (
                                    SELECT DISTINCT ON (callsign) velocity
                                    FROM aeroplanes
                                    );""")
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            avg_speed = self.__db_date_tuple_to_dict(columns, rows)
            return avg_speed

    def get_aeroplanes_with_higher_speed(self) -> list[dict]:
        """получает список всех самолетов, у которых скорость выше средней"""
        # получаем среднюю скорость по всем самолетам в виде: [{'aeroplanes_avg_velocity': 175.46884977852534}]
        avg_speed = self.get_avg_speed()
        with self.conn:
            self.cur.execute(
                """SELECT DISTINCT ON (callsign) * FROM aeroplanes
                                WHERE velocity > %s;""",
                (avg_speed[0]["aeroplanes_avg_velocity"],),
            )
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            aeroplanes_with_higher_speed = self.__db_date_tuple_to_dict(columns, rows)
            return aeroplanes_with_higher_speed

    def get_aeroplanes_with_keyword(self, search: str) -> list[dict]:
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        # если передана не строка, возвращаем пустой список
        if not isinstance(search, str):
            return []
        # если строка поиска длиннее callsign, возвращаем пустой список
        if len(search) > 8:
            return []
        # создаем шаблон для запроса и переводим в верхний регистр(позывные приходят в врехнем регистре)
        pattern = f"%{search.upper()}%"
        with self.conn:
            self.cur.execute(
                """SELECT DISTINCT ON (callsign) * FROM aeroplanes WHERE callsign  LIKE %s;""", (pattern,)
            )
            # получаем данные столбцов(строки)
            rows = self.cur.fetchall()
            # получаем имена столбцов
            columns = [column_names[0] for column_names in self.cur.description]
            # Преобразуем список картажей в список словарей для читаемости полученых данных
            aeroplanes_with_keyword = self.__db_date_tuple_to_dict(columns, rows)
            return aeroplanes_with_keyword

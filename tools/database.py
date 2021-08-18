import psycopg2
import os

if __name__ == "__main__":
    raise Exception()

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __start_conn(self):
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"])
        self.cursor = self.conn.cursor()

    def __end_conn(self):
        self.cursor.close()
        self.conn.close()

    def __end_conn_and_save(self):
        self.conn.commit()
        self.__end_conn()

    def execute(self, sql_query :str):
        """
        :param sql_query:
        :return: all results of that query
        """
        self.__start_conn()
        try:
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            output = results
        except psycopg2.Error as e:
            output = f"{e}"
        finally:
            self.__end_conn_and_save()
        return output


    def get_table(self, table_name :str, where="", order_by=""):
        """
        :param table_name: name of a table
        :param where: sql where eg. id = 2 AND number > 4
        :param order_by: sql order by eg. id, name
        :return: matching elements in table table_name
        """

        if order_by != "":
            order_by = "ORDER BY " + order_by

        if where != "":
            where = "WHERE " + where

        self.__start_conn()
        self.cursor.execute(f"""
            SELECT 
                *
            FROM
                {table_name}
            {where}
            {order_by}
        """)
        results = self.cursor.fetchall()
        self.__end_conn()
        return results

    def add_to_table(self, table_name :str, columns :str, values :str):
        """
        :param table_name:
        :param columns: col1, col2
        :param values: v1, v2
        :return:
        """
        self.__start_conn()
        self.cursor.execute(f"""
            INSERT INTO {table_name}({columns})
            VALUES ({values})
        """)
        self.__end_conn_and_save()

    def delete_from_table(self, table_name: str, where :str):
        """
        :param table_name:
        :param where:
        :return:
        """
        self.__start_conn()
        self.cursor.execute(f"""
               DELETE FROM {table_name}
               WHERE {where}
           """)
        self.__end_conn_and_save()

    def replace_in_table(self, table_name :str, columns :list, values :list, where :str = None):
        """
        :param table_name:
        :param columns:
        :param values:
        :param where:
        :return:
        """
        set_str = ""

        if len(columns) != len(values):
            raise AttributeError("Database: not the same amount of columns and values!")

        for i in range(len(columns)):
            set_str += f"{columns[i]} = {values[i]}"
            if i != len(columns) - 1:
                set_str += ","

        if where is not None:
            where = "WHERE " + where

        self.__start_conn()
        self.cursor.execute(f"""
            UPDATE {table_name}
            SET {set_str}
            {where}
        """)
        self.__end_conn_and_save()

    def create_table(self, table_name :str, columns :str):
        """
        :param table_name: table_name
        :param columns: table columns eg. id INT, name TEXT, number INT
        :return: None
        """
        self.__start_conn()
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                {columns}
            )
        """)
        self.__end_conn_and_save()

    def delete_table(self, table_name :str):
        """
        :param table_name:
        :return: None
        """
        self.__start_conn()
        self.cursor.execute(f"""
                    DROP TABLE {table_name}
                """)
        self.__end_conn_and_save()



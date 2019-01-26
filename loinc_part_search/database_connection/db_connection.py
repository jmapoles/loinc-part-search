# --------------------------------------------------------
# --------------------------------------------------------

import pymysql
import psycopg2

# --------------------------------------------------------
# --------------------------------------------------------


class DBConnection:
    """
    Database connection
    """

    def __init__(self, type , server, user_name, password, database):
        """
        :param type: database connection type, mysql or postgres
        :param server:
        :param user_name:
        :param password:
        :param database:

        """

        self.type = type

        if type == 'mysql':
            self.conn = pymysql.connect( host=server , user=user_name , password=password, database=database )
        elif type == 'postgres':
            self.conn = psycopg2.connect( host=server , user=user_name , password=password, dbname=database )
        else:
            raise Exception( " unknown connection type " )


    # --------------------------------------------------------

    def get_cursor(self):
        """
        :return: cursor

        return db cursor
        """
        return self.conn.cursor()


    def get_sql_cursor(self, sql_query):
        """
        :param sql_query:
        :return: cursor

        executes query and returns cursor for results
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        return cursor

    def execute_query(self, sql_insert ):
        """
        :param sql_insert:
        :return: cursor

        executes insert query and commits result
        """
        cursor = self.conn.cursor()
        cursor.execute(sql_insert)
        self.conn.commit()
        cursor.close()

    def commit(self):
        """
        wraps the commit method
        """
        self.conn.commit()

    def return_single_row(self, query ):
        """
        :param query:
        :return: first row or None

        """

        cursor = self.get_sql_cursor(query)
        if cursor.rowcount != 1:
           return None

        row = cursor.fetchone()
        cursor.close()

        return row


    # --------------------------------------------------------

    @staticmethod
    def escape_field(text):
        """
        :param text: input field
        :return: escaped text

        static method to escape text field, an ' is changed to ''
        """

        if text is None:
            return None

        text = text.replace("'", "''")
        return text


# --------------------------------------------------------
# --------------------------------------------------------

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch , MagicMock
from loinc_part_search.database_connection.db_connection import DBConnection



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestMySQLQuery(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        # mock the connection
        patcher = patch( "loinc_part_search.database_connection.db_connection.pymysql" )
        mock_pymysql  = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance and the cursor
        instance_py = mock_pymysql.return_value
        self.py_connection = instance_py.connect.return_value

        # QueryMySQLLOINC
        self.db_conn = DBConnection( "mysql" , "server", "user", "pass", "db" )
        self.db_conn.mysql = self.py_connection



    # --------------------------------------------------------------------------

    #
    #################
    def test_get_sql_cursor( self ):

        # will return MagicMock name='pymysql().connect().cursor()
        cursor = self.db_conn.get_sql_cursor( "" )

    #
    #################
    def test_execute_query( self ):

        # will return MagicMock name='pymysql().connect().cursor()
        cursor = self.db_conn.execute_query( "" )


    #
    #################
    def test_commit( self ):

        # will return MagicMock name='pymysql().connect().cursor()
        self.db_conn.commit( )


    #
    #################
    def test_return_single_row(self):

        test_list = []

        # Internal mock Mock
        self.py_connection.cursor.call_args_list.return_value = test_list
        self.py_connection.cursor.rowcount = len( test_list )
        # self.py_connection.cursor.fetchone.return_value = test_list[0]

        self.db_conn.get_sql_cursor = MagicMock()
        self.db_conn.get_sql_cursor.return_value = self.py_connection.cursor

        row = self.db_conn.return_single_row( "" )
        self.assertIsNone( row )


        test_list = [ [1] ]

        # Internal mock Mock
        self.py_connection.cursor.call_args_list.return_value = test_list
        self.py_connection.cursor.rowcount = len( test_list )
        self.py_connection.cursor.fetchone.return_value = test_list[0]

        row = self.db_conn.return_single_row ( "" )
        self.assertEqual ( row , test_list[0] )


        test_list = [ [1] , [2] ]

        # Internal mock Mock
        self.py_connection.cursor.call_args_list.return_value = test_list
        self.py_connection.cursor.rowcount = len( test_list )
        self.py_connection.cursor.fetchone.return_value = test_list[0]

        row = self.db_conn.return_single_row ( "" )
        self.assertIsNone ( row )


    #
    #################
    def test_escape_field(self):

        self.assertIsNone( self.db_conn.escape_field ( None ) )
        self.assertEqual( self.db_conn.escape_field( "" ) , "" )
        self.assertEqual( self.db_conn.escape_field( "'" ) , "''" )
        self.assertEqual( self.db_conn.escape_field( "'" ) , "''" )
        self.assertEqual( self.db_conn.escape_field( "'q" ) , "''q" )
        self.assertEqual( self.db_conn.escape_field( "q'" ) , "q''" )
        self.assertEqual( self.db_conn.escape_field( "q'q" ) , "q''q" )
        self.assertEqual( self.db_conn.escape_field( "q'q'q" ) , "q''q''q" )


    # --------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch
from loinc_part_search.database_connection.db_queries import QueryLOINC
from loinc_part_search.unittests.test_constants import TestConstants


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestMySQLQuery(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        # mock the connection
        patcher = patch( "loinc_part_search.database_connection.db_queries.DBConnection" )
        mock_mysql = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance and the cursor
        self.mysql = mock_mysql.return_value
        self.cursor = self.mysql.get_sql_cursor.return_value

        # QueryMySQLLOINC
        self.db_conn = QueryLOINC( "mysql" , "server" , "user" , "pass" , "db" )
        self.db_conn.mysql = self.mysql



    # --------------------------------------------------------------------------

    def test_get_obj_id_of_code_type( self ):

        self.mysql.return_single_row.return_value = TestConstants.return_of_obj_id_query[0]

        obj_id = self.db_conn.get_obj_id_of_code_type( "code definition", "10000-9" )

        self.assertEqual( obj_id, 0 )


    # --------------------------------------------------------------------------

    def test_obj_id_exists( self  ):

        self.cursor.rowcount = 1

        id_exists = self.db_conn.obj_id_exists( 0 )

        self.assertTrue( id_exists )


    # --------------------------------------------------------------------------

    def test_get_defining_attributes_of_obj_id(self):

        self.mysql.return_single_row.return_value = TestConstants.return_of_obj_id_query[0]

        defining_attributes = self.db_conn.get_defining_attributes_of_obj_id ( 0 )

        self.assertEqual( defining_attributes , ( 1 , '10000-9') )


    # --------------------------------------------------------------------------

    def test_get_attributes_of_obj_id( self):

        self.cursor.fetchall.return_value = TestConstants.return_of_attribute_query

        attributes = self.db_conn.get_attributes_of_obj_id ( 0 )
        self.assertEqual( attributes , TestConstants.return_of_attribute_method )


    def test_get_attributes_of_obj_id_no_return( self):

        self.cursor.fetchall.return_value = TestConstants.return_of_empty_attribute_query

        attributes = self.db_conn.get_attributes_of_obj_id ( 0 )

        self.assertEqual( attributes , TestConstants.return_of_empty_attribute_method )


    # --------------------------------------------------------------------------

    def test_get_parents_of_obj_id( self):

        self.cursor.fetchall.return_value = TestConstants.return_of_parents_query

        parents = self.db_conn.get_parent_ids_of_obj_id( 0 )

        self.assertEqual( parents , TestConstants.return_of_parents_method )


    def test_get_children_of_obj_id( self):

        self.cursor.fetchall.return_value = TestConstants.return_of_children_query

        parents = self.db_conn.get_child_ids_of_obj_id( 0 )

        self.assertEqual( parents , TestConstants.return_of_children_method )


    def test_get_ancestors_of_obj_id( self):

        self.cursor.fetchall.return_value = TestConstants.return_of_ancestor_query

        ancestors = self.db_conn.get_ancestor_ids_of_obj_id( 0 )

        self.assertEqual( ancestors , TestConstants.return_of_ancestor_method )


    def test_get_ancestors_of_obj_id_to_level(self):

        self.cursor.fetchall.return_value = TestConstants.return_of_ancestor_level_query

        ancestors = self.db_conn.get_ancestor_ids_of_obj_id_to_level ( 0, 3 )

        self.assertEqual ( ancestors, TestConstants.return_of_ancestor_level_method )


    def test_get_descendants_of_id(self):

        self.cursor.fetchall.return_value = TestConstants.return_of_descendant_query

        ancestors = self.db_conn.get_descendant_ids_of_id( 40 )

        self.assertEqual ( ancestors, TestConstants.return_of_descendant_method )


    # --------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

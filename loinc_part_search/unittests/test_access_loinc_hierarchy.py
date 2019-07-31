# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch , MagicMock
from loinc_part_search.db_data.access_loinc_hierarchy import AccessLOINCHierarchy
from loinc_part_search.unittests.test_constants import TestConstants


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestAccessLOINCHiearchy(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        patcher = patch( "loinc_part_search.db_data.access_loinc_connection.QueryLOINC" )
        mock_db_conn = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance
        self.db_conn = mock_db_conn.return_value

        self.access_loinc = AccessLOINCHierarchy( "type" , "server", "user", "pass", "db" , "schema" )
        self.access_loinc.db_conn = self.db_conn


    # --------------------------------------------------------------------------

    def test_add_obj_to_list(self):

        list_of_ids = []

        # mock up get_dictionary_of_obj_id
        self.access_loinc.get_eav_obj_of_id = MagicMock()
        self.access_loinc.get_eav_obj_of_id.side_effect = [ ]

        list_of_objects = self.access_loinc.add_obj_to_list( list_of_ids )

        self.assertEqual( len( list_of_objects ) , 0 )


        list_of_ids = [ TestConstants.obj_id_1001 ]

        # mock up get_dictionary_of_obj_id
        self.access_loinc.get_eav_obj_of_id.side_effect = [ TestConstants.part_1001 ]

        list_of_objects = self.access_loinc.add_obj_to_list( list_of_ids )

        self.assertEqual( len( list_of_objects ) , 1 )
        self.assertEqual( list_of_objects[0].name_and_code_str(), TestConstants.name_1001 )


        list_of_ids = [ TestConstants.obj_id_1001 , TestConstants.obj_id_1001 ]

        # mock up get_dictionary_of_obj_id
        self.access_loinc.get_eav_obj_of_id.side_effect = [ TestConstants.part_1001 ]

        list_of_objects = self.access_loinc.add_obj_to_list( list_of_ids )

        self.assertEqual( len( list_of_objects ) , 1 )
        self.assertEqual( list_of_objects[0].name_and_code_str(), TestConstants.name_1001 )


        list_of_ids = [ TestConstants.obj_id_1001 , TestConstants.obj_id_1002 ]

        # mock up get_dictionary_of_obj_id
        self.access_loinc.get_eav_obj_of_id.side_effect = \
                [ TestConstants.part_1001 , TestConstants.part_1002 ]

        list_of_objects = self.access_loinc.add_obj_to_list( list_of_ids )

        self.assertEqual( len( list_of_objects ) , 2 )
        self.assertEqual( list_of_objects[0].name_and_code_str(), TestConstants.name_1001 )
        self.assertEqual ( list_of_objects[1].name_and_code_str (), TestConstants.name_1002 )


    def test_get_parent_obj_of_id(self):

        # mock up get_dictionary_of_obj_id
        self.access_loinc.obj_id_exists = MagicMock()
        self.access_loinc.obj_id_exists.return_value = True

        self.access_loinc.add_obj_to_list = MagicMock()
        self.access_loinc.add_obj_to_list.return_value = [TestConstants.part_1001]

        parents = self.access_loinc.get_parent_obj_of_id( TestConstants.obj_id_1003 )

        self.assertEqual( len( parents ) , 1 )
        self.assertEqual( parents[0].name_and_code_str() , TestConstants.name_1001 )


    def test_get_child_obj_of_id(self):

        # mock up get_dictionary_of_obj_id
        self.access_loinc.obj_id_exists = MagicMock()
        self.access_loinc.obj_id_exists.return_value = True

        self.access_loinc.add_obj_to_list = MagicMock()
        self.access_loinc.add_obj_to_list.return_value = [TestConstants.part_1001]

        parents = self.access_loinc.get_child_obj_of_id( TestConstants.obj_id_1003 )

        self.assertEqual( len( parents ) , 1 )
        self.assertEqual( parents[0].name_and_code_str() , TestConstants.name_1001 )


    def test_get_ancestors_obj_of_id(self):
        # mock up get_dictionary_of_obj_id
        self.access_loinc.obj_id_exists = MagicMock ()
        self.access_loinc.obj_id_exists.return_value = True

        self.access_loinc.add_obj_to_list = MagicMock ()
        self.access_loinc.add_obj_to_list.return_value = [TestConstants.part_1001]

        parents = self.access_loinc.get_ancestors_obj_of_id ( TestConstants.obj_id_1003 )

        self.assertEqual ( len ( parents ), 1 )
        self.assertEqual ( parents[0].name_and_code_str (), TestConstants.name_1001 )


    def test_get_descendants_obj_of_id(self):
        # mock up get_dictionary_of_obj_id
        self.access_loinc.obj_id_exists = MagicMock ()
        self.access_loinc.obj_id_exists.return_value = True

        self.access_loinc.add_obj_to_list = MagicMock ()
        self.access_loinc.add_obj_to_list.return_value = [TestConstants.part_1001]

        parents = self.access_loinc.get_descendants_obj_of_id ( TestConstants.obj_id_1003 )

        self.assertEqual ( len ( parents ), 1 )
        self.assertEqual ( parents[0].name_and_code_str (), TestConstants.name_1001 )


    def test_get_ancestors_obj_of_id_to_level(self):

        # mock up get_dictionary_of_obj_id
        self.access_loinc.obj_id_exists = MagicMock()
        self.access_loinc.obj_id_exists.return_value = True

        self.access_loinc.get_parent_obj_of_id = MagicMock()
        self.access_loinc.get_parent_obj_of_id.return_value = [ TestConstants.part_1001 ]

        self.access_loinc.add_obj_to_list = MagicMock()
        self.access_loinc.add_obj_to_list.return_value = \
                [ TestConstants.part_1001 , TestConstants.part_1000 ]

        ancestors = self.access_loinc.get_ancestors_obj_of_id_to_level( TestConstants.obj_id_1003 , 0 )
        self.assertEqual( len( ancestors ) , 0 )

        ancestors = self.access_loinc.get_ancestors_obj_of_id_to_level( TestConstants.obj_id_1003 , 1 )
        self.assertEqual( len( ancestors ) , 1 )
        self.assertEqual( ancestors[0].name_and_code_str() , TestConstants.name_1001 )

        ancestors = self.access_loinc.get_ancestors_obj_of_id_to_level( TestConstants.obj_id_1003 , 2 )
        self.assertEqual( len( ancestors ) , 2 )
        self.assertEqual( ancestors[0].name_and_code_str() , TestConstants.name_1001 )
        self.assertEqual( ancestors[1].name_and_code_str() , TestConstants.name_1000 )


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

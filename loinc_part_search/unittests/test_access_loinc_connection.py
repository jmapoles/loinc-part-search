# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch
from loinc_part_search.db_data.access_loinc_eav_object import AccessLOINCObj
from loinc_part_search.unittests.test_constants import TestConstants
from loinc_part_search.database_connection.attribute_type_definitions import AttributeTypeDefinitions

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestAccessLOINCConnection(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        patcher = patch( "loinc_part_search.db_data.access_loinc_connection.QueryLOINC" )
        mock_db_conn = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance
        self.db_conn = mock_db_conn.return_value

        # AccessLOINC
        self.access_loinc = AccessLOINCObj( "type" , "server", "user", "pass", "db" , "schema" )
        self.access_loinc.db_conn = self.db_conn

        self.access_loinc.attribute_type_definitions: AttributeTypeDefinitions = AttributeTypeDefinitions()

        self.access_loinc.attribute_type_definitions.add_attribute_type_definition_with_id( 1 , "Name", "name" )
        self.access_loinc.attribute_type_definitions.add_attribute_type_definition_with_id( 2 , "LOINC Code" , "value")
        self.access_loinc.attribute_type_definitions.add_attribute_type_definition_with_id( 3 , "LOINC Part Code" , "value")


    # --------------------------------------------------------------------------

    #####
    def test_object_id_exists( self ):

        self.db_conn.obj_id_exists.return_value = True
        self.assertTrue( self.access_loinc.obj_id_exists( "" ) )


    #####
    def test_get_attributes_of_obj_id(self):

        # Mock
        self.db_conn.get_attributes_of_obj_id.return_value = TestConstants.attributes_1003

        attributes = self.access_loinc.get_attributes_of_obj_id( TestConstants.obj_id_1003 )
        self.assertEqual ( len( attributes ) , len( TestConstants.attributes_1003 ) )


    #####
    def test_get_defining_attributes_of_obj_id(self):

        # Mock
        self.db_conn.get_defining_attributes_of_obj_id.return_value = TestConstants.defining_attribute_1003

        defining_attribute = self.access_loinc.get_defining_attributes_of_obj_id( TestConstants.obj_id_1003 )
        self.assertEqual ( defining_attribute , TestConstants.defining_attribute_1003 )


    #####
    def test_get_parent_ids_of_obj_id(self):

        self.db_conn.get_parent_ids_of_obj_id.return_value = TestConstants.parents_1003

        parents = self.access_loinc.get_parent_ids_of_obj_id( TestConstants.obj_id_1003 )
        self.assertEqual ( len( parents ) , len( TestConstants.parents_1003 ) )


    #####
    def test_get_child_ids_of_obj_id(self):

        self.db_conn.get_child_ids_of_obj_id.return_value = TestConstants.children_1003

        children = self.access_loinc.get_child_ids_of_obj_id ( TestConstants.obj_id_1003 )
        self.assertEqual ( len ( children ), len ( TestConstants.children_1003 ) )

    #####
    def test_get_ancestor_ids_of_obj_id(self):

        self.db_conn.get_ancestor_ids_of_obj_id.return_value = TestConstants.parents_1003

        ancestors = self.access_loinc.get_ancestor_ids_of_obj_id ( TestConstants.obj_id_1003 )
        self.assertEqual ( len ( ancestors ), len ( TestConstants.parents_1003 ) )


    #####
    def test_get_ancestor_ids_of_obj_id_to_level(self):

        self.db_conn.get_ancestor_ids_of_obj_id_to_level.return_value = TestConstants.parents_1003

        children = self.access_loinc.get_ancestor_ids_of_obj_id_to_level ( TestConstants.obj_id_1003 , 2 )
        self.assertEqual ( len ( children ), len ( TestConstants.parents_1003 ) )


    #####
    def test_get_descendant_ids_of_id(self):

        self.db_conn.get_descendant_ids_of_id.return_value = TestConstants.children_1003

        children = self.access_loinc.get_descendant_ids_of_id ( TestConstants.obj_id_1003 )
        self.assertEqual ( len ( children ), len ( TestConstants.children_1003 ) )



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

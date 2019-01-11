# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch
from loinc_part_search.db_data.access_loinc_eav_object import AccessLOINCObj
from loinc_part_search.unittests.test_constants import TestConstants


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestAccessLOINCObjects(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        patcher = patch( "loinc_part_search.db_data.access_loinc_connection.QueryLOINC" )
        mock_db_conn = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance
        self.db_conn = mock_db_conn.return_value

        # AccessLOINC
        self.access_loinc = AccessLOINCObj( "type" , "server", "user", "pass", "db" )
        self.access_loinc.db_conn = self.db_conn



    # --------------------------------------------------------------------------

    def test_get_eav_obj_of_id( self ):


        # Mocks
        #
        # id exists
        self.db_conn.obj_id_exists.return_value = True
        # defining attributes
        self.db_conn.get_defining_attributes_of_obj_id.return_value = \
            (TestConstants.defining_attribute_id_1003 , TestConstants.defining_value_1003 )
        # attributes
        self.db_conn.get_attributes_of_obj_id.return_value = TestConstants.attributes_db_1003
        # parents
        self.db_conn.get_parent_ids_of_obj_id.return_value = TestConstants.parents_1003
        # children
        self.db_conn.get_child_ids_of_obj_id.return_value = TestConstants.children_1003
        #
        #################################


        test_obj = self.access_loinc.get_eav_obj_of_id( TestConstants.obj_id_1003 )


        self.assertEqual( test_obj.get_obj_id() , TestConstants.obj_id_1003 )
        self.assertEqual( test_obj.get_defining_attribute()[0] , TestConstants.defining_attribute_name_1003 )
        self.assertEqual( test_obj.get_defining_attribute()[1] , TestConstants.defining_value_1003 )
        self.assertEqual( test_obj.get_parents() , TestConstants.parents_1003 )
        self.assertEqual( test_obj.get_children() , TestConstants.children_1003 )
        self.assertEqual ( test_obj.get_preferred_id_value() , TestConstants.code_1003 )
        attributes = test_obj.get_attributes()
        self.assertEqual ( len( attributes ) , len( TestConstants.attributes_1003 ) )

        for attribute_definition in attributes:

            self.assertTrue( attribute_definition in TestConstants.attributes_1003 )
            self.assertEqual( attributes[attribute_definition] , TestConstants.attributes_1003[ attribute_definition] )



    def test_get_eav_obj_of_code(self ):

        # Mock
        self.db_conn.get_obj_id_of_code_type.return_value = TestConstants.obj_id_1003

        test_obj = self.access_loinc.get_eav_obj_of_code( TestConstants.code_1003 )
        self.assertEqual( test_obj.get_obj_id() , TestConstants.obj_id_1003 )


    def test_get_eav_obj_of_part_code(self ):

        # Mock
        self.db_conn.get_obj_id_of_code_type.return_value = TestConstants.obj_id_1003

        test_obj = self.access_loinc.get_eav_obj_of_part_code( TestConstants.code_1003 )
        self.assertEqual( test_obj.get_obj_id() , TestConstants.obj_id_1003 )




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

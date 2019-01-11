# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch
from loinc_part_search.db_data.access_loinc import AccessLOINC
from loinc_part_search.unittests.test_constants import TestConstants
from unittest.mock import MagicMock

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestAccessLOINC(unittest.TestCase):

    # --------------------------------------------------------------------------

    def setUp(self):

        patcher = patch( "loinc_part_search.db_data.access_loinc_connection.QueryLOINC" )
        mock_db_conn = patcher.start()
        self.addCleanup ( patcher.stop )

        # mocked instance
        self.db_conn = mock_db_conn.return_value

        self.access_loinc = AccessLOINC( "type" , "server", "user", "pass", "db" )
        self.access_loinc.db_conn = self.db_conn


    # --------------------------------------------------------------------------

    def test_get_descendants_obj_of_id_as_map( self ):

        all_objects = [ TestConstants.part_1001 , TestConstants.part_1001 , \
                        TestConstants.part_1003 , TestConstants.part_1004 , \
                        TestConstants.code_1006 , TestConstants.code_1009 , \
                        TestConstants.code_1007 , TestConstants.code_1010 ]

        all_ids = { TestConstants.obj_id_1001 , TestConstants.obj_id_1003 , TestConstants.obj_id_1004 , \
              TestConstants.obj_id_1006 , TestConstants.obj_id_1009 , TestConstants.obj_id_1007 , \
              TestConstants.obj_id_1010 }

        self.db_conn.obj_id_exists.return_value = True

        self.access_loinc.object_id_exists = MagicMock()
        self.access_loinc.object_id_exists.return_value = True

        self.access_loinc.get_descendant_ids_of_id = MagicMock()
        self.access_loinc.get_descendant_ids_of_id.return_value = all_ids

        self.access_loinc.get_eav_obj_of_id = MagicMock()
        self.access_loinc.get_eav_obj_of_id.side_effect = all_objects


        desc_objs = self.access_loinc.get_descendants_obj_of_id_as_map( TestConstants.obj_id_1001 )

        self.assertTrue( desc_objs.size() , len( all_ids ) )

        for desc_id in desc_objs.get_keys():

            self.assertIn( desc_id , all_ids )



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

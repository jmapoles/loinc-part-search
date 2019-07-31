# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from unittest.mock import patch , MagicMock
from loinc_part_search.db_data.access_json import AccessJSON
from loinc_part_search.unittests.test_constants import TestConstants
import json

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class TestAccessJSON(unittest.TestCase):

    # --------------------------------------------------------------------------


    def setUp(self):

        patcher = patch( "loinc_part_search.db_data.access_json.AccessLOINC" )
        self.access_loinc = patcher.start()
        self.addCleanup ( patcher.stop )

        self.json = AccessJSON( self.access_loinc )


    # --------------------------------------------------------------------------

    def check_eav_dictionary(self, eav_dict):

        self.assertEqual ( eav_dict['defining definition'], 'LOINC Part Code' )
        self.assertEqual ( eav_dict['LOINC Part Code'], '1003' )
        self.assertEqual ( eav_dict['preferred attribute'], 'Name' )
        self.assertEqual ( eav_dict['Name'], 'LP-1003' )

        self.assertEqual ( eav_dict['Common rank'], '0' )
        self.assertEqual ( eav_dict['Short name'], 'R wave dur L-AVR' )
        self.assertEqual ( eav_dict['Class type'], '2' )
        self.assertEqual ( eav_dict['Status'], 'ACTIVE' )

        self.assertEqual ( eav_dict['parents'], \
                           [TestConstants.name_1001] )
        self.assertEqual ( eav_dict['children'], \
                           [TestConstants.name_1006,TestConstants.name_1009] )


    def test_get_dictionary_of_eav_obj( self ):

        self.json.access.get_eav_obj_of_id.side_effect = \
                [
                    TestConstants.part_1001 ,
                    TestConstants.code_1006 ,
                    TestConstants.code_1009
                ]

        self.json.access.get_eav_obj_of_code.return_value = TestConstants.obj_id_1003
        eav_dict = self.json.get_dictionary_of_eav_obj( TestConstants.part_1003 )
        self.check_eav_dictionary( eav_dict )


    def test_get_json_of_loinc_code( self ):

        self.json.access.get_eav_obj_of_id.side_effect = \
                [
                    TestConstants.part_1001,
                    TestConstants.code_1006,
                    TestConstants.code_1009
                ]
        self.json.access.get_eav_obj_of_code.return_value = TestConstants.part_1003
        json_str = self.json.get_json_of_loinc_code( TestConstants.obj_id_1003 )
        self.check_eav_dictionary( json.loads( json_str ) )


    def test_get_json_of_loinc_part_code(self):

        self.json.access.get_eav_obj_of_id.side_effect = \
            [
                TestConstants.part_1001,
                TestConstants.code_1006,
                TestConstants.code_1009
            ]
        self.json.access.get_eav_obj_of_part_code.return_value = TestConstants.part_1003
        json_str = self.json.get_json_of_loinc_part_code ( TestConstants.obj_id_1003 )
        self.check_eav_dictionary ( json.loads ( json_str ) )



    def test_get_json_of_obj_id(self):

        self.json.access.get_eav_obj_of_id.side_effect = \
            [
                TestConstants.part_1003,
                TestConstants.part_1001,
                TestConstants.code_1006,
                TestConstants.code_1009
            ]
        self.json.access.get_eav_obj_of_id.return_value = TestConstants.part_1003
        json_str = self.json.get_json_of_obj_id ( TestConstants.obj_id_1003 )
        self.check_eav_dictionary ( json.loads ( json_str ) )


    def test_get_dictionary_of_loinc_code(self):

        self.json.access.get_eav_obj_of_id.side_effect = \
            [
                TestConstants.part_1001,
                TestConstants.code_1006,
                TestConstants.code_1009
            ]
        self.json.access.get_eav_obj_of_code.return_value = TestConstants.part_1003
        dict_str = self.json.get_dictionary_of_loinc_code ( TestConstants.obj_id_1003 )
        self.check_eav_dictionary ( dict_str )


    def test_get_dictionary_of_obj_id(self):

        self.json.access.get_eav_obj_of_id.side_effect = \
            [
                TestConstants.part_1003,
                TestConstants.part_1001,
                TestConstants.code_1006,
                TestConstants.code_1009
            ]
        self.json.access.get_eav_obj_of_id.return_value = TestConstants.part_1003
        dict_str = self.json.get_dictionary_of_obj_id ( TestConstants.obj_id_1003 )
        self.check_eav_dictionary ( dict_str )


    def test_get_json_parents_of_obj_id(self):

        self.json.access.get_parent_ids_of_obj_id.return_value = TestConstants.part_1003.get_parents()

        # mock up get_dictionary_of_obj_id
        self.json.get_dictionary_of_obj_id = MagicMock()
        self.json.get_dictionary_of_obj_id.return_value = TestConstants.dict_1001

        json_str = self.json.get_json_parents_of_obj_id ( TestConstants.obj_id_1003 )
        json_str_dict = json.loads( json_str )
        self.assertEqual( len( json_str_dict ) , 1 )
        self.assertTrue( json_str_dict[0] == TestConstants.dict_1001 )


    def test_get_json_descendant_of_loinc_part_code(self):

        self.json.access.get_obj_id_of_code_type.return_value = TestConstants.obj_id_1000
        self.json.access.get_descendants_obj_of_id_as_map.return_value = TestConstants.eav_map

        json_str = self.json.get_json_descendant_of_loinc_part_code ( '1000' )
        json_dict = json.loads( json_str )

        self.assertTrue( json_dict == TestConstants.dict_map)


    def test_get_json_siblings_of_loinc_code(self):

        self.json.access.get_obj_id_of_code_type.return_value = TestConstants.obj_id_1006
        self.json.access.get_parent_ids_of_obj_id.return_value = TestConstants.code_1006.get_parents()
        self.json.access.get_child_ids_of_obj_id.return_value = \
            { TestConstants.obj_id_1006 , TestConstants.obj_id_1009 }

        # mock up get_dictionary_of_obj_id
        self.json.get_dictionary_of_obj_id = MagicMock()
        self.json.get_dictionary_of_obj_id.side_effect = \
            [ TestConstants.dict_1006 , TestConstants.dict_1009 ]


        json_str = self.json.get_json_siblings_of_loinc_code( 'L-1006' )
        json_dict = json.loads( json_str )

        self.assertTrue( json_dict == [ TestConstants.dict_1006 , TestConstants.dict_1009 ] )






    def test_get_json_cousins_of_loinc_code(self):

        self.json.access.get_obj_id_of_code_type.return_value = TestConstants.obj_id_1006
        self.json.access.get_ancestor_ids_of_obj_id_to_level.return_value = { TestConstants.obj_id_1003 , TestConstants.obj_id_1001 }
        self.json.access.get_descendant_ids_of_id.side_effect = \
            [ { TestConstants.obj_id_1003 , TestConstants.obj_id_1006 , TestConstants.obj_id_1009 } , \
              { TestConstants.obj_id_1001 , TestConstants.obj_id_1003 , TestConstants.obj_id_1006 , TestConstants.obj_id_1009 , TestConstants.obj_id_1007 , TestConstants.obj_id_1010 } ]
        self.json.access.get_eav_obj_of_id.side_effect = \
                [ TestConstants.part_1001 , TestConstants.part_1003 , TestConstants.code_1006 , TestConstants.code_1007 , TestConstants.code_1009 , TestConstants.code_1010 ]

        # mock up get_dictionary_of_obj_id
        self.json.get_dictionary_of_eav_obj = MagicMock()
        self.json.get_dictionary_of_eav_obj.side_effect = \
            [ TestConstants.dict_1006 , TestConstants.dict_1007 , TestConstants.dict_1009 , TestConstants.dict_1010 ]


        json_str = self.json.get_json_cousins_of_loinc_code( 'L-1006' )
        json_dict = json.loads( json_str )

        self.assertTrue ( json_dict == [ TestConstants.dict_1006 , TestConstants.dict_1007 , TestConstants.dict_1009 , TestConstants.dict_1010 ] )





# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

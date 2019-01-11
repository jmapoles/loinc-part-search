# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.loinc_part_api.loinc_json_flask import app
from loinc_part_search.unittests.test_constants import TestConstants
import unittest
from unittest.mock import patch
import json
from flask import Flask


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class TestAccessJSON( unittest.TestCase ):

    # --------------------------------------------------------------------------

    def setUp( self ):
        # create that app
        self.app = app

        # Mock the AccessJSON
        patcher = patch( "loinc_part_search.loinc_part_api.loinc_json_flask.access" )
        mock_access = patcher.start()

        self.app.testing = True
        self.client = app.test_client()
        self.client.access = mock_access
        self.addCleanup( patcher.stop )

    def test_index( self ):
        rv = self.client.get( '/' )
        self.assertEqual( rv.status_code , 200 )
        self.assertEqual( rv.data, b'<h1>LOINC Part search</h1>' )

    def test_loinc( self ):
        # Mock
        self.client.access.get_json_of_loinc_code.return_value = \
            json.dumps( TestConstants.dict_1003 )

        rv = self.client.get( '/loinc/' + str( TestConstants.code_1003 ) )

        self.assertEqual( rv.status_code , 200 )

        self.assertTrue( json.loads( rv.data ) == TestConstants.dict_1003 )

    def test_loinc_siblings( self ):
        # Mock
        self.client.access.get_json_siblings_of_loinc_code.return_value = \
            json.dumps( [ TestConstants.dict_1006, TestConstants.dict_1009 ] )

        rv = self.client.get( '/loinc/siblings/' + str( TestConstants.code_1006 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == [ TestConstants.dict_1006, \
                                                    TestConstants.dict_1009 ] )

    def test_loinc_cousins( self ):
        # Mock
        self.client.access.get_json_cousins_of_loinc_code.return_value = \
            json.dumps( [ TestConstants.dict_1006, TestConstants.dict_1009, \
                          TestConstants.dict_1007, TestConstants.dict_1010 ] )

        rv = self.client.get( '/loinc/cousins/' + str( TestConstants.code_1006 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == [ TestConstants.dict_1006, \
                                                    TestConstants.dict_1009, TestConstants.dict_1007, \
                                                    TestConstants.dict_1010 ] )

    def test_loinc_parents( self ):
        # Mock
        self.client.access.get_json_parents_of_loinc_code.return_value = \
            json.dumps( [ TestConstants.dict_1003 ] )

        rv = self.client.get( '/loinc/parents/' + str( TestConstants.code_1006 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == [ TestConstants.dict_1003 ] )

    def test_loinc_parts( self ):
        # Mock
        self.client.access.get_json_of_loinc_part_code.return_value = \
            json.dumps( TestConstants.dict_1003 )

        rv = self.client.get( '/loinc/parts/' + str( TestConstants.code_1003 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == TestConstants.dict_1003 )

    def test_loinc_part_descendants( self ):
        # Mock
        self.client.access.get_json_descendant_of_loinc_part_code.return_value = \
            json.dumps( [ TestConstants.dict_1006, TestConstants.dict_1009 ] )

        rv = self.client.get( '/loinc/parts/descendants/' + str( TestConstants.code_1006 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == [ TestConstants.dict_1006, TestConstants.dict_1009 ] )

    def test_loinc_part_parents( self ):
        # Mock
        self.client.access.get_json_parents_of_loinc_part_code.return_value = \
            json.dumps( [ TestConstants.dict_1001 ] )

        rv = self.client.get( '/loinc/parts/parents/' + str( TestConstants.code_1006 ) )

        self.assertEqual( rv.status_code , 200 )
        self.assertTrue( json.loads( rv.data ) == [ TestConstants.dict_1001 ] )

    def test_404( self ):
        rv = self.client.get( '/other' )
        self.assertEqual( rv.status, '404 NOT FOUND' )


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

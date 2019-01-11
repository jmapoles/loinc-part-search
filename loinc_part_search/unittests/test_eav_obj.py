# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

import unittest
from loinc_part_search.loinc_objects.eav_objects import EAVObject, EAVMap

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class TestEAVObject(unittest.TestCase):

    def test_empty_object(self):

        eav_obj = EAVObject()

        self.assertIsNone( eav_obj.get_obj_id() )
        self.assertIsNone( eav_obj.get_preferred_id() )

        parents = eav_obj.get_parents()
        children = eav_obj.get_children()
        attributes = eav_obj.get_attributes()

        self.assertTrue( isinstance(parents, set) )
        self.assertEqual( len(parents) , 0 )
        self.assertTrue( isinstance(children, set) )
        self.assertEqual( len(children) , 0 )
        self.assertTrue( isinstance(attributes, dict) )
        self.assertEqual( len(attributes) , 0 )


    def test_initial_with_id(self):

        eav_obj = EAVObject("test")
        self.assertIsNone( eav_obj.get_obj_id() )

        eav_obj = EAVObject(-1)
        self.assertIsNone ( eav_obj.get_obj_id () )

        eav_obj = EAVObject(1)
        self.assertEqual( eav_obj.get_obj_id() , 1 )

        eav_obj = EAVObject ( 1 , None , '1111' , None , 'name-1111')
        self.assertEqual ( eav_obj.get_obj_id (), 1 )

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 0 )
        preferred_attribute = eav_obj.get_preferred_id ()
        self.assertIsNone( preferred_attribute )
        defining_attribute = eav_obj.get_defining_attribute()
        self.assertEqual( defining_attribute , () )


        eav_obj = EAVObject ( 1 , 1 , '1111' , 'Name' , 'name-1111')
        self.assertEqual ( eav_obj.get_obj_id (), 1 )

        attributes = eav_obj.get_attributes ()
        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]
        preferred_attribute = eav_obj.get_preferred_id ()

        self.assertEqual( attribute_definition , 'Name' )
        self.assertEqual( attribute_value , 'name-1111')
        self.assertEqual( preferred_attribute , 'Name' )

        defining_attribute = eav_obj.get_defining_attribute()

        self.assertEqual( defining_attribute[0] , 1 )
        self.assertEqual( defining_attribute[1] , "1111" )


    def test_id(self):

        eav_obj = EAVObject(1)

        self.assertEqual( eav_obj.get_obj_id() , 1 )
        eav_obj.set_obj_id(2)
        self.assertEqual( eav_obj.get_obj_id() , 2 )

        eav_obj.clear_obj_id ()
        self.assertIsNone ( eav_obj.get_obj_id () )


    def test_parents(self):

        eav_obj = EAVObject(1)

        eav_obj.add_parent("")

        parents = eav_obj.get_parents()
        self.assertEqual( len(parents) , 0 )


        eav_obj.add_parent( -2 )

        parents = eav_obj.get_parents()
        self.assertEqual( len(parents) , 0 )


        eav_obj.add_parent(2)

        parents = eav_obj.get_parents()
        first_parent = list(parents)[0]
        self.assertEqual( len(parents) , 1 )
        self.assertEqual( first_parent , 2 )

        eav_obj.clear_parents()
        parents = eav_obj.get_parents()
        self.assertEqual( len(parents) , 0 )


    def test_child(self):

        eav_obj = EAVObject(1)


        eav_obj.add_child("")

        children = eav_obj.get_children()
        self.assertEqual( len(children) , 0 )


        eav_obj.add_child( -2 )

        children = eav_obj.get_children()
        self.assertEqual( len(children) , 0 )


        eav_obj.add_child(3)

        children = eav_obj.get_children()
        first_parent = list(children)[0]
        self.assertEqual( len(children) , 1 )
        self.assertEqual( first_parent , 3 )

        eav_obj.clear_children()
        children = eav_obj.get_children()
        self.assertEqual( len(children) , 0 )


    def test_attributes(self):

        eav_obj = EAVObject(1)

        # will fail definition cannot be none
        eav_obj.add_attribute ( None , "test" )

        attributes = eav_obj.get_attributes ()
        self.assertEqual( len ( attributes ) , 0 )

        # will fail definition cannot be empty
        eav_obj.add_attribute ( "" , "test" )

        attributes = eav_obj.get_attributes ()
        self.assertEqual( len ( attributes ) , 0 )


        # will succeed definition can be negative
        eav_obj.add_attribute ( -4 , "test 1" )

        attributes = eav_obj.get_attributes ()
        self.assertEqual( len ( attributes ) , 1 )

        eav_obj.clear_attributes()


        # no change same attribute
        eav_obj.add_attribute ( -4, "test 1" )

        attributes = eav_obj.get_attributes ()
        self.assertEqual ( len ( attributes ), 1 )

        eav_obj.clear_attributes ()


        # one attribute but not a preferred definition
        eav_obj.add_attribute(4, "test 1")

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 1 )

        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]
        preferred_attribute = eav_obj.get_preferred_id ()

        self.assertEqual( attribute_definition , 4 )
        self.assertEqual( attribute_value , "test 1" )
        self.assertIsNone( preferred_attribute )


        # now two attributes
        eav_obj.add_attribute(5, "test 2")

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 2 )

        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]

        self.assertEqual( attribute_definition , 4 )
        self.assertEqual( attribute_value , "test 1" )

        attribute_definition = list(attributes.keys())[1]
        attribute_value = attributes[attribute_definition]

        self.assertEqual( attribute_definition , 5 )
        self.assertEqual( attribute_value , "test 2" )


        # clear removes all attributes
        eav_obj.clear_attributes()
        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 0 )


        # adding attribute that is preferred
        eav_obj.add_attribute ( 6, "test 6" , True  )

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 1 )

        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]
        preferred_attribute = eav_obj.get_preferred_id()

        self.assertEqual( attribute_definition , 6 )
        self.assertEqual( attribute_value , "test 6" )
        self.assertEqual( preferred_attribute , 6 )


        # adding attribute as a tuple
        eav_obj.clear_attributes ()
        eav_obj.clear_preferred_id()
        attr_tuple = ( 6, "test 6" )
        eav_obj.add_attribute_tuple( attr_tuple )

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 1 )

        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]
        preferred_attribute = eav_obj.get_preferred_id()


        self.assertEqual( attribute_definition , 6 )
        self.assertEqual( attribute_value , "test 6" )
        self.assertEqual( preferred_attribute , None )


        # adding attributes as a list of tuples
        eav_obj.clear_attributes ()
        eav_obj.clear_preferred_id()
        attr_tuple1 = ( 6, "test 6" )
        attr_tuple2 = ( 7, "test 7")
        attr_list = [ attr_tuple1 , attr_tuple2 ]
        eav_obj.add_attributes( attr_list )

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 2 )

        attribute_definition1 = list(attributes.keys())[0]
        attribute_value1 = attributes[attribute_definition1]

        attribute_definition2 = list ( attributes.keys () )[1]
        attribute_value2 = attributes[attribute_definition2]

        preferred_attribute = eav_obj.get_preferred_id()


        self.assertEqual( attribute_definition1 , 6 )
        self.assertEqual( attribute_value1 , "test 6" )

        self.assertEqual( attribute_definition2 , 7 )
        self.assertEqual( attribute_value2 , "test 7" )


        self.assertEqual( preferred_attribute , None )


    def test_defining_attribute(self):

        eav_obj = EAVObject(1)
        eav_obj.set_defining_attribute( 1 , "code 1")

        defining_attribute = eav_obj.get_defining_attribute()

        self.assertEqual( defining_attribute[0] , 1 )
        self.assertEqual( defining_attribute[1] , "code 1" )


        eav_obj.set_defining_attribute( 2 , "code 2")

        defining_attribute = eav_obj.get_defining_attribute()

        self.assertEqual( defining_attribute[0] , 2 )
        self.assertEqual( defining_attribute[1] , "code 2" )


        eav_obj.clear_defining_attribute()

        defining_attribute = eav_obj.get_defining_attribute()

        self.assertEqual( defining_attribute , () )


    def test_defining_attribute_and_name(self):

        eav_obj = EAVObject(1)
        eav_obj.set_defining_attribute_and_name( 1 , "code 1" , 6, "test 6" )

        defining_attribute = eav_obj.get_defining_attribute()

        self.assertEqual( defining_attribute[0] , 1 )
        self.assertEqual( defining_attribute[1] , "code 1" )

        attributes = eav_obj.get_attributes()
        self.assertEqual( len(attributes) , 1 )

        attribute_definition = list(attributes.keys())[0]
        attribute_value = attributes[attribute_definition]
        preferred_attribute = eav_obj.get_preferred_id()

        self.assertEqual( attribute_definition , 6 )
        self.assertEqual( attribute_value , "test 6" )
        self.assertEqual( preferred_attribute , 6 )



    def test_preferred_id(self):

        eav_obj = EAVObject ( 1 )

        preferred_id = eav_obj.get_preferred_id()
        self.assertEqual( preferred_id , None )


        eav_obj.set_attribute_as_preferred( 1 )

        preferred_id = eav_obj.get_preferred_id()
        self.assertEqual( preferred_id , None )


        eav_obj.add_attribute( 1 , "test 1" )
        eav_obj.add_attribute( 2 , "test 2" )

        eav_obj.set_attribute_as_preferred( 1 )

        preferred_id = eav_obj.get_preferred_id()
        self.assertEqual( preferred_id , 1 )

        eav_obj.set_attribute_as_preferred( 2 )

        preferred_id = eav_obj.get_preferred_id()
        self.assertEqual( preferred_id , 2 )
        self.assertEqual( eav_obj.is_preferred( 2 ) , True )
        self.assertNotEqual( eav_obj.is_preferred ( 1 ), True )

        eav_obj.clear_preferred_id()
        preferred_id = eav_obj.get_preferred_id()
        self.assertEqual( preferred_id , None )


    def test_eav_map(self):
        """
        Test the map.  Add three objects
        1. test size of map is 3
        2. Get the object assigned to key 1 and test id is 1
        3. Get list of object and test size is 3
        4. Add 2 and 3 as children of 1 test that 1 has no parents
        5. refactor parents test that 2 has one parent and 1 has no parents
        """

        eav_obj1 = EAVObject(1)
        eav_obj2 = EAVObject(2)
        eav_obj3 = EAVObject(3)

        eav_map = EAVMap()
        eav_map.add(1, eav_obj1)
        eav_map.add(2, eav_obj2)
        eav_map.add(3, eav_obj3)

        self.assertEqual(eav_map.size() , 3 )

        eav_obj_test = eav_map.get_eav_object(1)
        self.assertEqual(eav_obj_test.get_obj_id() , 1 )

        eav_list = eav_map.get_eav_objects()
        self.assertEqual(len(eav_list) , 3 )

        eav_obj1.add_child(2)
        eav_obj1.add_child(3)

        self.assertEqual( len(eav_obj2.get_parents()) , 0 )

        eav_map.refactor_parent_child()

        self.assertEqual( len(eav_obj2.get_parents()) , 1 )
        self.assertEqual( len(eav_obj1.get_parents()) , 0 )


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

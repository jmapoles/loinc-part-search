# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from typing import List


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class EAVObject:
    """
    EAVObject is the core object used to hold data from database queries.
    """


    # ------------------------------------------------

    def __init__(self, obj_id=None , defining_definition=None , defining_value=None , attribute_definition=None , attribute_value=None ):
        """
        Initialize the object.  Can be built without values including the object id.

        :param obj_id:
        """

        self.obj_id = None
        if type( obj_id ) is int and obj_id > -1:
            self.obj_id = obj_id

        self.preferred_id = None
        self.defining_attribute = tuple()
        self.parents = set()
        self.children = set()
        self.attributes = dict()

        self.set_defining_attribute_and_name( defining_definition , defining_value , attribute_definition , attribute_value )

    # ------------------------------------------------

    def set_obj_id(self, obj_id):
        """
        Add an object id value. Must be can int greater than -1.
        :param obj_id:
        """

        if type( obj_id ) is int and obj_id > -1:
            self.obj_id = obj_id

    def get_obj_id(self):
        """
        Get the object id
        :return: the object id
        """
        return self.obj_id

    def clear_obj_id(self):
        """
        Remove object id value
        """
        self.obj_id = None

    # ------------------------------------------------

    def add_parent(self, parent_id):
        """
        Add a parent, must be an int and greater that -1.
        :param parent_id:
        """
        if type( parent_id ) is int and parent_id > -1:
            self.parents.add(parent_id)

    def get_parents(self):
        """
        get the parent set
        :return: parent set
        """
        return self.parents

    def clear_parents(self):
        """
        Empty the parent set
        """
        self.parents = set()


    # ------------------------------------------------

    def add_child(self, child_id):
        """
        Add a child, must be and integer greater that -1.
        :param child_id:
        """

        if type( child_id ) is int and child_id > -1:
            self.children.add(child_id)

    def get_children(self):
        """
        Return the children set.
        :return: children set.
        """
        return self.children

    def clear_children(self):
        """
        Empty the children set
        """
        self.children = set()


    # ------------------------------------------------

    def add_attribute(self, attribute_definition, attribute_value , preferred=None ):
        """
        Adds an attribute. Current model is limited to one value per definition.
        Definition cannot be None or empty.  Value may be.
        :param attribute_definition:
        :param attribute_value:
        :param preferred: boolean, if true this attribute definition is set as the preferred attribute
        """

        if attribute_definition is None:
            return

        if not attribute_definition:
            return

        # don't add an attribute twice
        if attribute_definition in self.attributes:

            if self.attributes[attribute_definition] == attribute_value:

                return


        self.attributes[attribute_definition] = attribute_value
        if preferred:
            self.set_attribute_as_preferred( attribute_definition )

    def add_attribute_tuple(self, attribute ):
        """
        Adds an attribute tuple
        :param attribute:
        """

        if len( attribute ) == 2:
            self.add_attribute( attribute[0] , attribute[1] )

    def add_attributes(self, attributes:List ):
        """
        Adds a list of attribute tuples
        :param attributes :
        """

        for attribute in attributes:
            self.add_attribute_tuple( attribute )


    def get_attributes(self):
        """
        Get the attributes dictionary.
        :return: Attributes dictionary.
        """
        return self.attributes

    def clear_attributes(self):
        """
        Empty the attributes dictionary
        """
        self.attributes = dict()

    # ------------------------------------------------

    def set_defining_attribute(self, attribute_definition, attribute_value):
        """
        Sets the defining attribute of the object. Neither can be None or empty
        :param attribute_definition:
        :param attribute_value:
        """

        if attribute_definition is None:
            return
        if not attribute_definition:
            return

        if attribute_value is None:
            return
        if not attribute_value:
            return

        self.defining_attribute = (attribute_definition, attribute_value)


    def get_defining_attribute(self) -> tuple:
        """
        Returns the defining attribute tuple
        :return: defining attribute tuple
        """

        return self.defining_attribute

    def clear_defining_attribute(self):
        """
        Empty the defining attribute tuple
        """
        self.defining_attribute = tuple()



    # ------------------------------------------------

    def set_defining_attribute_and_name(self, defining_definition, defining_value , attribute_definition, attribute_value ):
        """
        Add both the defining attribute and the preferred attribute.
        :param defining_definition:
        :param defining_value:
        :param attribute_definition:
        :param attribute_value:
        :return:
        """

        if defining_definition is None:
            return

        if not defining_definition:
            return
        self.set_defining_attribute ( defining_definition, defining_value )

        if attribute_definition is None:
            return

        if not attribute_definition:
            return
        self.add_attribute( attribute_definition , attribute_value , True )



    # ------------------------------------------------

    def get_preferred_id_value(self):
        """
        Get the value specified by the preferred id.
        Value may be None if it has not been set.
        Value is stored in the attributes dictionary, the value self.attributes[self.preferred_id] is returned.
        :return: Attributes value for the preferred id key
        """
        if self.preferred_id is None:
            return None

        return self.attributes[self.preferred_id]


    def set_attribute_as_preferred(self, preferred_id):
        """
        Set the preferred id, must be an existing attribute
        :param preferred_id:
        """
        if preferred_id in self.attributes:
            self.preferred_id = preferred_id


    def get_preferred_id(self):
        """
        Get the preferred id itself.  This is a attributes key.
        Use get_preferred_id_value() to get the value associated with this key.
        :return: preferred id
        """
        return self.preferred_id


    def is_preferred(self, preferred_id):
        """
        Check if this value is the preferred id.
        :param preferred_id:
        :return: Boolean
        """
        if self.preferred_id is None:
            return False

        if self.preferred_id == preferred_id:
            return True

        return False

    def clear_preferred_id(self):
        """
        Removed preferred id, set to None.
        """
        self.preferred_id = None


    # ------------------------------------------------

    def display(self,level=5):
        """
        Used for testing etc. Prints a description to console.
        :param level:
        :return: String display
        """
        defining_definition = self.defining_attribute[0]
        defining_value = self.defining_attribute[1]


        print("Defining attribute: " + str(defining_definition) + ": " + str(defining_value))
        print("Preferred attribute: " + str(self.get_preferred_id_value() ))
        print( "Object id: " + str ( self.get_obj_id() ) )

        preferred_attribute_definition = self.get_preferred_id()


        if level > 0:

            for attribute_definition in self.attributes.keys():

                if attribute_definition == preferred_attribute_definition:
                    continue


                print("    " + str(attribute_definition) + ": " + str(self.attributes[attribute_definition]))

        if level > 1:

            if len( self.parents ) == 0:
                print( "Parents: none")
            else:
                for parent in self.parents:
                    print("Parent: " + str(parent) )


        if level > 2:

            if len( self.children ) == 0:
                print( "Children: none")
            else:
                for child in self.children:
                    print("Child: " + str(child) )


    def name_and_code_str(self):
        """
        Returns the name and code as a string.
        :return: Name and code as string
        """
        defining_definition = self.defining_attribute[0]
        defining_value = self.defining_attribute[1]


        return str ( defining_definition ) + ": " + str ( defining_value ) + ", " +str ( self.get_preferred_id_value() )


    # ------------------------------------------------
    # ------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class EAVMap:
    """
    EAVMap holds EAVObjects as a dictionary
    Each entry is a key value pair of obj_id and the EAVObj
    """

    # ------------------------------------------------

    def __init__(self):
        """
        Creates the map as a dictionary
        """
        self.map = dict()

    # ------------------------------------------------

    def add(self, obj_id, obj: EAVObject):
        """
        adds a object id EAVObject pair to the map
        :param obj_id:
        :param obj:
        """
        self.map[obj_id] = obj

    def get_eav_object(self, obj_id):
        """
        Return the EAVObject stored for the obj_id key.
        Returns None is the obj_id is not a key.
        :param obj_id:
        :return: EAVObject in the map
        """
        if obj_id in self.map:
            return self.map[obj_id]
        return None

    def has_obj_id(self, obj_id) -> bool:
        """
        Returns True is the obj_id is a key in the map and false over wise.
        :param obj_id:
        :return: Boolean
        """
        if obj_id in self.map:
            return True
        return False

    # ------------------------------------------------

    def get_keys(self) -> List:
        """
        Return a list of all keys in the map.
        :return: list of keys
        """
        return list(self.map.keys())

    def get_eav_objects(self) -> List:
        """
        Returns a list of all the EAVObject stored as values in the map.
        :return: list of EAVObject values
        """
        return list(self.map.values())

    # ------------------------------------------------

    def clear(self) -> None:
        """
        Empties the map
        """
        self.map.clear()

    def clear_obj_id(self, obj_id) -> None:
        """
        Removed obj_id from the map.
        :param obj_id:
        """
        if self.has_obj_id(obj_id):
            self.map.pop(obj_id, None)

    def size(self) -> int:
        """
        Returns the number of keys
        :return: Length or number of keys.
        """
        return len(self.map)

    # ------------------------------------------------

    def refactor_parent_child(self) -> None:
        """
        Ensures that all hierarchical relation in the map are listed as parents and children
        """
        for key in self.get_keys():

            eav_obj = self.get_eav_object(key)

            parents = eav_obj.get_parents()
            for obj_id in parents:

                if self.has_obj_id(obj_id):
                    eav_parent = self.get_eav_object(obj_id)
                    eav_parent.add_child(key)

        for key in self.get_keys():

            eav_obj = self.get_eav_object(key)

            children = eav_obj.get_children()
            for obj_id in children:

                if self.has_obj_id(obj_id):
                    eav_child = self.get_eav_object(obj_id)
                    eav_child.add_parent(key)


    def display_as_hierarchy(self):
        """
        Used for testing prints to console an indented list of the map hierarchy.
        Printing starts with objects without parents.  The object and all descendants are printed.
        Objects with parents that are not in the map are printed with all descendants.
        Any object not printed are added at the end.
        """
        # keep track of what was displayed
        displayed = set()


        # displays descendants and keeps track of what was displayed
        def display_of_id( obj , tab ):

            displayed.add( obj.get_obj_id() )
            print( tab + obj.name_and_code_str() )
            for child_id in obj.get_children():

                if self.has_obj_id( child_id ):

                    child_obj = self.map.get ( child_id )
                    display_of_id( child_obj , tab + "   " )

                else:

                    print( tab + "unk id: " + str( child_id ) )



        for key in self.get_keys():

            eav_obj = self.get_eav_object ( key )


            # object without parents
            if len( eav_obj.get_parents() ) == 0:

                display_of_id( eav_obj , "" )

            else:

                parents = eav_obj.get_parents()
                no_parents_in_map = True

                for parent_id in parents:

                    if self.has_obj_id( parent_id ):

                        no_parents_in_map = False

                # object with parents that are not in the map
                if no_parents_in_map:

                    display_of_id( eav_obj, "" )

        # any unprinted objects
        for key in self.get_keys():

            if key not in displayed:

                eav_obj = self.get_eav_object ( key )
                print ( eav_obj.name_and_code_str () )


    # ------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.loinc_objects.eav_objects import EAVObject
from loinc_part_search.db_data.access_loinc import AccessLOINC
from loinc_part_search.loinc_objects.loinc_eav_constants import LOINCEAVConstants
import json


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class AccessJSON:
    """
    EAV objects returned as json
    """

    # --------------------------------------------------------

    def __init__(self,access:AccessLOINC):

        self.access = access


    # --------------------------------------------------------

    def get_json_of_loinc_code(self, loinc_code):

        eav_obj = self.access.get_eav_obj_of_code( loinc_code )
        if eav_obj is None:
            return json.dumps ( {} )

        return json.dumps ( self.get_dictionary_of_eav_obj ( eav_obj ) )

    def get_json_of_loinc_part_code(self, loinc_part_code):

        eav_obj = self.access.get_eav_obj_of_part_code( loinc_part_code )
        if eav_obj is None:
            return json.dumps ( {} )

        return json.dumps ( self.get_dictionary_of_eav_obj ( eav_obj ) )

    def get_json_of_obj_id(self, obj_id):

        eav_obj = self.access.get_eav_obj_of_id ( obj_id )
        if eav_obj is None:
            return json.dumps ( {} )

        return json.dumps ( self.get_dictionary_of_eav_obj ( eav_obj ) )

    def get_dictionary_of_loinc_code(self, loinc_code):

        eav_obj = self.access.get_eav_obj_of_code( loinc_code )
        if eav_obj is None:
            return {}

        return self.get_dictionary_of_eav_obj( eav_obj )

    def get_dictionary_of_obj_id(self, obj_id):

        eav_obj = self.access.get_eav_obj_of_id ( obj_id )
        if eav_obj is None:
            return {}

        return self.get_dictionary_of_eav_obj( eav_obj )

    # --------------------------------------------------------

    def get_dictionary_of_eav_obj(self , eav_obj:EAVObject ):

        object_dictionary = dict()


        defining_definition = eav_obj.defining_attribute[0]
        defining_value = eav_obj.defining_attribute[1]
        preferred_attribute_definition = eav_obj.get_preferred_id()

        object_dictionary[ "defining definition" ] = defining_definition
        object_dictionary[ defining_definition ] = defining_value


        for attribute_definition in eav_obj.attributes.keys ():

            if attribute_definition == preferred_attribute_definition:

                object_dictionary["preferred attribute"] = preferred_attribute_definition
                object_dictionary[preferred_attribute_definition] = eav_obj.get_preferred_id_value()


        for attribute_definition in eav_obj.attributes.keys ():

            if attribute_definition == preferred_attribute_definition:
                continue

            object_dictionary[attribute_definition] = eav_obj.attributes[attribute_definition]




        parents = []
        for parent in eav_obj.parents:

            if self.access.obj_id_exists( parent ):


                # create the object
                parent_obj = self.access.get_eav_obj_of_id ( parent )

                parents.append( parent_obj.name_and_code_str() )


        object_dictionary[ "parents"] = parents



        children = []
        for child in eav_obj.children:

            if self.access.obj_id_exists ( child ):

                # create the object
                child_obj = self.access.get_eav_obj_of_id ( child )

                children.append ( child_obj.name_and_code_str () )


        object_dictionary[ "children"] = children


        return object_dictionary


    # --------------------------------------------------------

    def get_json_parents_of_loinc_code(self , loinc_code ):

        obj_id = self.access.get_obj_id_of_code_type( LOINCEAVConstants.loinc_code_definition , loinc_code )
        if obj_id is None:
            return json.dumps ( {} )

        return self.get_json_parents_of_obj_id ( obj_id )


    def get_json_parents_of_loinc_part_code(self, loinc_part_code):

        obj_id = self.access.get_obj_id_of_code_type( LOINCEAVConstants.loinc_part_definition , loinc_part_code )
        if obj_id is None:
            return json.dumps ( {} )

        return self.get_json_parents_of_obj_id( obj_id )

    def get_json_parents_of_obj_id(self , obj_id ):

        # set parents as object id
        parent_ids = self.access.get_parent_ids_of_obj_id ( obj_id )


        # get json for each parent
        parents = list ()
        for parent_id in parent_ids:
            parents.append ( self.get_dictionary_of_obj_id ( parent_id ) )

        return json.dumps ( parents )


    # --------------------------------------------------------

    def get_json_descendant_of_loinc_part_code(self , loinc_part_code ):

        part_id = self.access.get_obj_id_of_code_type( LOINCEAVConstants.loinc_part_definition , loinc_part_code )
        if part_id is None:
            return json.dumps ( {} )

        eav_map = self.access.get_descendants_obj_of_id_as_map ( part_id )


        # recursive building of dictionary
        def add_children_to_dictionary( obj_id ):

            loinc_obj = eav_map.get_eav_object ( obj_id )
            loinc_name = loinc_obj.name_and_code_str ()


            children = loinc_obj.get_children()
            if len( children ) == 0:

                return loinc_name

            else:

                local_dict = dict()
                local_list = list()
                for child_id in children:

                    local_list.append ( add_children_to_dictionary( child_id ) )

                local_dict[ loinc_name ] = local_list

                return local_dict

        ####################################



        # get map and top object

        descendants = add_children_to_dictionary( part_id )

        return json.dumps( descendants )




    # --------------------------------------------------------

    def get_json_siblings_of_loinc_code(self , loinc_code ):

        obj_id = self.access.get_obj_id_of_code_type( LOINCEAVConstants.loinc_code_definition , loinc_code )
        if obj_id is None:
            return json.dumps ( {} )


        # set parents as object id
        parent_ids = self.access.get_parent_ids_of_obj_id( obj_id )


        # find all children
        children = set()
        for parent_id in parent_ids:

            children = children | self.access.get_child_ids_of_obj_id( parent_id )


        # get json for each child
        sibling = list()
        for child in children:

            sibling.append( self.get_dictionary_of_obj_id( child ) )


        return json.dumps( sibling )



    # --------------------------------------------------------

    def get_json_cousins_of_loinc_code(self , loinc_code ):

        obj_id = self.access.get_obj_id_of_code_type( LOINCEAVConstants.loinc_code_definition , loinc_code )
        if obj_id is None:
            return json.dumps ( {} )


        # set parents as object id
        ancestors = self.access.get_ancestor_ids_of_obj_id_to_level( obj_id , 2 )


        # find all descendants
        descendants = set()
        for ancestor_id in ancestors:

            descendants = descendants | self.access.get_descendant_ids_of_id( ancestor_id )


        # loinc_code_str is "LOINC Code"
        loinc_code_str = LOINCEAVConstants.constant_names[ LOINCEAVConstants.loinc_code_definition ]


        # get json for loinc descendants
        cousins = list()
        for loinc_child_id in descendants:

            loinc_eav_obj = self.access.get_eav_obj_of_id( loinc_child_id )
            defining_attribute = loinc_eav_obj.get_defining_attribute()[0]

            if defining_attribute == loinc_code_str:
                cousins.append( self.get_dictionary_of_eav_obj( loinc_eav_obj ))

        return json.dumps( cousins )


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

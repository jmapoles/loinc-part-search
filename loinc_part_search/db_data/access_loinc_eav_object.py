# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.loinc_objects.eav_objects import EAVObject
from loinc_part_search.loinc_objects.loinc_eav_constants import  LOINCEAVConstants
from loinc_part_search.db_data.access_loinc_connection import AccessLOINCConnection

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class AccessLOINCObj( AccessLOINCConnection ):
    """
    Access query_db database and return object based on id and LOINC code
    """


    # --------------------------------------------------------


    def get_eav_obj_of_id(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVObj from obj_id with all attributes, parents, and children
        """


        # check if the id exists
        if not self.db_conn.obj_id_exists( obj_id ):
            return None


        # create the object
        eav_obj = EAVObject( obj_id )


        # add all other attributes
        for attribute in self.db_conn.get_attributes_of_obj_id( obj_id ):

            if attribute[0] in LOINCEAVConstants.constant_names:

                attribute_definition = LOINCEAVConstants.constant_names[attribute[0]]

                eav_obj.add_attribute( attribute_definition,attribute[1])
                if attribute[2] == 1:
                    eav_obj.set_attribute_as_preferred( attribute_definition )


        # add defining attributes
        defining_attributes = self.db_conn.get_defining_attributes_of_obj_id( obj_id )

        if defining_attributes[0] in LOINCEAVConstants.constant_names:
            defining_definition = LOINCEAVConstants.constant_names[defining_attributes[0]]
            defining_value = defining_attributes[1]

            eav_obj.set_defining_attribute( defining_definition , defining_value )


        # add parents
        for parent in self.db_conn.get_parent_ids_of_obj_id( obj_id ):

            eav_obj.add_parent ( parent )


        # add children
        for children in self.db_conn.get_child_ids_of_obj_id( obj_id ):

            eav_obj.add_child ( children )


        return eav_obj


    # --------------------------------------------------------


    def get_eav_obj_of_code(self, loinc_code):
        """
        :param loinc_code:
        :return: EAVObj, None

        Builds an EAVObj from loinc_code with all attributes, parents, and children
        """

        obj_id = self.db_conn.get_obj_id_of_code_type( LOINCEAVConstants.loinc_code_definition, loinc_code )
        if obj_id is None:
            return None

        return self.get_eav_obj_of_id( obj_id )


    def get_eav_obj_of_part_code(self, loinc_part_code):
        """
        :param loinc_part_code:
        :return: EAVObj, None

        Builds an EAVObj from loinc_code with all attributes, parents, and children
        """

        obj_id = self.db_conn.get_obj_id_of_code_type( LOINCEAVConstants.loinc_part_definition, loinc_part_code )
        if obj_id is None:
            return None

        return self.get_eav_obj_of_id( obj_id )


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

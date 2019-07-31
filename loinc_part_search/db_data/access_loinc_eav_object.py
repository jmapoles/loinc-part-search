# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.loinc_objects.eav_objects import EAVObject
from loinc_part_search.db_data.access_loinc_connection import AccessLOINCConnection

from loinc_part_search.database_connection.attribute_type_definition import AttributeTypeDefinition


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class AccessLOINCObj( AccessLOINCConnection ):
    """
    Access query_db database and return object based on id and LOINC code
    """

    loinc_code_name = 'LOINC Code'
    loinc_part_code_name = 'LOINC Part Code'

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
        for attribute_row in self.db_conn.get_attributes_of_obj_id( obj_id ):

            if self.attribute_type_definitions.attribute_type_definition_id_exits( attribute_row[0] ):

                attribute_type_definition: AttributeTypeDefinition = \
                    self.attribute_type_definitions.get_attribute_type_using_id( attribute_row[0] )

                attribute_name = attribute_type_definition.get_attribute_name()
                attribute_value = attribute_row[1]
                attribute_preferred = attribute_row[ 2 ]

                # TODO: can be done in one step eav_obj.add_attribute( attribute_name,attribute_value,attribute_preferred)
                eav_obj.add_attribute( attribute_name,attribute_value)
                if attribute_preferred == 1:
                    eav_obj.set_attribute_as_preferred( attribute_name )


        # add defining attributes
        defining_attributes = self.db_conn.get_defining_attributes_of_obj_id( obj_id )

        if self.attribute_type_definitions.attribute_type_definition_id_exits( defining_attributes[0] ):
            attribute_type_definition: AttributeTypeDefinition = \
                self.attribute_type_definitions.get_attribute_type_using_id( defining_attributes[ 0 ] )

            defining_name = attribute_type_definition.get_attribute_name()
            defining_value = defining_attributes[ 1 ]

            eav_obj.set_defining_attribute( defining_name , defining_value )


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

        loinc_code_definition : AttributeTypeDefinition = self.attribute_type_definitions.get_attribute_type_using_name( AccessLOINCObj.loinc_code_name )
        loinc_code_definition_id = loinc_code_definition.get_attribute_id()


        obj_id = self.db_conn.get_obj_id_of_code_type( loinc_code_definition_id , loinc_code )
        if obj_id is None:
            return None

        return self.get_eav_obj_of_id( obj_id )


    def get_eav_obj_of_part_code(self, loinc_part_code):
        """
        :param loinc_part_code:
        :return: EAVObj, None

        Builds an EAVObj from loinc_code with all attributes, parents, and children
        """

        loinc_part_code_definition : AttributeTypeDefinition = self.attribute_type_definitions.get_attribute_type_using_name( AccessLOINCObj.loinc_part_code_name )
        loinc_part_code_definition_id = loinc_part_code_definition.get_attribute_id()

        obj_id = self.db_conn.get_obj_id_of_code_type( loinc_part_code_definition_id , loinc_part_code )
        if obj_id is None:
            return None

        return self.get_eav_obj_of_id( obj_id )


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

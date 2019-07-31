# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.db_data.access_loinc_eav_object import AccessLOINCObj


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class AccessLOINCHierarchy( AccessLOINCObj ):

    # --------------------------------------------------------

    def get_parent_obj_of_id(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVObj from obj_id with all attributes, parents, and children
        """


        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return None


        return self.add_obj_to_list( self.get_parent_ids_of_obj_id( obj_id ) )


    def get_child_obj_of_id(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVObj from obj_id with all attributes, parents, and children
        """


        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return None

        return self.add_obj_to_list ( self.get_child_ids_of_obj_id ( obj_id ) )


    # --------------------------------------------------------

    def get_ancestors_obj_of_id(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVObj from obj_id with all attributes, parents, and children
        """


        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return None

        return self.add_obj_to_list ( self.get_ancestor_ids_of_obj_id ( obj_id ) )


    def get_ancestors_obj_of_id_to_level(self, obj_id, level:int):
        """
        :param obj_id:
        :param level:
        :return:
        """


        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return None

        ancestors = list ()


        if level < 1:
            return ancestors

        if level == 1:
            return self.get_parent_obj_of_id( obj_id )

        return self.add_obj_to_list( self.get_ancestor_ids_of_obj_id_to_level ( obj_id , level ) )



    def get_descendants_obj_of_id(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVObj from obj_id with all attributes, parents, and children
        """


        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return None

        return self.add_obj_to_list ( self.get_descendant_ids_of_id ( obj_id ) )



    def add_obj_to_list(self,list_of_id):
        """
        Takes a list of ids and returns a unique list of eav objects.
        Used by all the methods in this class.
        :param list_of_id:
        :return: unique list of eav objects
        """
        list_of_object = list ()
        set_of_ids = set ()  # set of id to ensure unique list
        for obj_id in list_of_id:

            if obj_id in set_of_ids:
                continue

            list_of_object.append ( self.get_eav_obj_of_id ( obj_id ) )
            set_of_ids.add ( obj_id )

        return list_of_object

    # --------------------------------------------------------



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

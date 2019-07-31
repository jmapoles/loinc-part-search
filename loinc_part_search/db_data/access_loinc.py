# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.db_data.access_loinc_hierarchy import AccessLOINCHierarchy
from loinc_part_search.loinc_objects.eav_objects import EAVMap

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class AccessLOINC( AccessLOINCHierarchy ):

    # --------------------------------------------------------

    def get_descendants_obj_of_id_as_map(self, obj_id):
        """
        :param obj_id:
        :return: EAVObj, None

        Builds an EAVMap of all the descendants
        """


        desc_map = EAVMap()

        # check if the id exists
        if not self.obj_id_exists( obj_id ):
            return map

        # add it to the map
        obj = self.get_eav_obj_of_id ( obj_id )
        desc_map.add ( obj_id, obj )


        descendants = self.get_descendant_ids_of_id( obj_id )
        if descendants is None:
            return desc_map

        # get parent ids
        for descendant_id in descendants:

            if desc_map.has_obj_id( descendant_id ):
                continue

            descendant_obj = self.get_eav_obj_of_id( descendant_id )
            desc_map.add( descendant_id , descendant_obj )


        return desc_map



    # --------------------------------------------------------



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

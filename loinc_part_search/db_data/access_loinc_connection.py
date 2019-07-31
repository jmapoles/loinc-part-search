# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.database_connection.db_queries import QueryLOINC
from loinc_part_search.database_connection.data_sources import DataSources
from loinc_part_search.database_connection.attribute_type_definitions import AttributeTypeDefinitions


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


class AccessLOINCConnection:
    """
    Access query_db database and return object based on id and LOINC code
    """

    # --------------------------------------------------------

    def __init__(self, type , server, user_name, password, database , schema ):

        self.type = type
        self.server = server
        self.user_name = user_name
        self.password = password
        self.database = database
        self.schema = schema

        self.db_conn = None


    def make_connection(self):

        self.db_conn = QueryLOINC( self.type , self.server , self.user_name , self.password , self.database , self.schema )
        self.db_conn.create_connection()

        self.data_sources: DataSources = self.db_conn.data_sources
        self.attribute_type_definitions : AttributeTypeDefinitions = self.db_conn.attribute_type_definitions


    # --------------------------------------------------------

    def get_obj_id_of_code_type(self, attribute_definition, code ):
        return self.db_conn.get_obj_id_of_code_type ( attribute_definition, code )

    def obj_id_exists(self, obj_id):
        return self.db_conn.obj_id_exists ( obj_id )

    def get_attributes_of_obj_id(self , obj_id ):
        return self.db_conn.get_attributes_of_obj_id ( obj_id )

    def get_defining_attributes_of_obj_id(self , obj_id ):
        return self.db_conn.get_defining_attributes_of_obj_id ( obj_id )

    def get_parent_ids_of_obj_id(self, obj_id):
        return self.db_conn.get_parent_ids_of_obj_id ( obj_id )

    def get_child_ids_of_obj_id(self, obj_id):
        return self.db_conn.get_child_ids_of_obj_id( obj_id )

    def get_ancestor_ids_of_obj_id(self, obj_id):
        return self.db_conn.get_ancestor_ids_of_obj_id ( obj_id )

    def get_ancestor_ids_of_obj_id_to_level(self, obj_id, level):
        return self.db_conn.get_ancestor_ids_of_obj_id_to_level ( obj_id, level )

    def get_descendant_ids_of_id(self, obj_id):
        return self.db_conn.get_descendant_ids_of_id( obj_id )

    def change_schema( self, schema ):
        self.db_conn.change_schema( schema )


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

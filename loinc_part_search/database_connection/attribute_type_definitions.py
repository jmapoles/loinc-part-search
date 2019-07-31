# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.database_connection.attribute_type_definition import AttributeTypeDefinition
from loinc_part_search.database_connection.db_connection import DBConnection

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class AttributeTypeDefinitions:
    """
    List of attribute type definitions
    """


    # ------------------------------------------------

    def __init__( self ):

        self.attribute_type_ids = {}
        self.attribute_type_names = {}

    def add_database_connection(self, db:DBConnection):
        """
        connect to database
        """
        self.db = db

        if not self.db.schema_exists( 'sources' ):
            raise Exception( " schema sources does not exist " )

        if not self.db.table_exists( 'sources', 'attribute_type_definitions' ):
            raise Exception( " table attribute_type_definitions does not exist " )


        query = f" select * from sources.attribute_type_definitions "
        cursor = self.db.get_sql_cursor(query)

        for row in cursor.fetchall():

            self.add_attribute_type_definition_with_id( row[0] , row[1] , row[2] )

        cursor.close()


    def add_attribute_type_definitions( self, attribute_name , attribute_type ):

        attribute_id = self.add_attribute_type_definition( attribute_name , attribute_type )

        if attribute_id > -1:

            query = f" insert into sources.attribute_type_definitions values( {attribute_id} , '{attribute_name}' , '{attribute_type}' )"
            self.db.execute_query( query )


    # ------------------------------------------------

    def add_attribute_type_definition( self, attribute_name , attribute_type ):
        """
        Add a DataSource object
        :param attribute_name:
        :param attribute_type:
        :return:
        """


        if self.attribute_type_definition_name_exits( attribute_name ): return -1

        attribute_id = max( self.attribute_type_ids.keys() ) + 1

        attribute_type = AttributeTypeDefinition( attribute_id , attribute_name , attribute_type  )

        self.attribute_type_ids[ attribute_id ] = attribute_type
        self.attribute_type_names[ attribute_name ] = attribute_type

        return attribute_id


    def add_attribute_type_definition_with_id( self, attribute_id , attribute_name , attribute_type ):
        """
        Add a DataSource object
        :param attribute_id:
        :param attribute_name:
        :param attribute_type:
        :return:
        """


        if self.attribute_type_definition_name_exits( attribute_name ): return -1
        if self.attribute_type_definition_id_exits( attribute_id ): return -1

        attribute_type = AttributeTypeDefinition( attribute_id , attribute_name , attribute_type  )

        self.attribute_type_ids[ attribute_id ] = attribute_type
        self.attribute_type_names[ attribute_name ] = attribute_type

        return attribute_id


    # ------------------------------------------------

    def delete_data_source( self, attribute_id ):

        if self.attribute_type_definition_id_exits( attribute_id ):

            attribute_name = self.get_attribute_type_definition_name( attribute_id )
            del self.attribute_type_ids[ attribute_id ]
            del self.attribute_type_names[ attribute_name ]


    # ------------------------------------------------

    def attribute_type_definition_id_exits( self, attribute_id ):
        """
        check if the attribute type definition exits
        :param attribute_id:
        """

        return attribute_id in self.attribute_type_ids


    # ------------------------------------------------

    def attribute_type_definition_name_exits( self, attribute_name ):
        """
        check if the attribute type definition name exits
        :param attribute_name:
        """

        return attribute_name in self.attribute_type_names


    # ------------------------------------------------

    def get_attribute_type_using_id( self , attribute_id ):

        if self.attribute_type_definition_id_exits( attribute_id ):

            return self.attribute_type_ids[ attribute_id ]

        return None


    # ------------------------------------------------

    def get_attribute_type_using_name( self , attribute_name ):

        if self.attribute_type_definition_name_exits( attribute_name ):

            return self.attribute_type_names[ attribute_name ]

        return None


    # ------------------------------------------------

    def get_attribute_type_definition_name( self, attribute_id ):
        """
        return name base on id
        :param attribute_id:
        """

        if attribute_id in self.attribute_type_ids:

            return self.attribute_type_ids[attribute_id].get_attribute_name()

        return None


    # ------------------------------------------------

    def get_attribute_type_definition_id( self, attribute_name ):
        """
        return name base on id
        :param attribute_name:
        """

        if attribute_name in self.attribute_type_names:

            return self.attribute_type_names[attribute_name].get_attribute_id()

        return None


    # ------------------------------------------------

    def get_attribute_types( self ):

        return self.attribute_type_ids.values()


    # ------------------------------------------------

    def source_count( self ):

        return len( self.attribute_type_ids )


    # ------------------------------------------------
    # ------------------------------------------------


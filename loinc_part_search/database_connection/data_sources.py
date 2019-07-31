# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.database_connection.data_source import DataSource
from loinc_part_search.database_connection.db_connection import DBConnection

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class DataSources:
    """
    List of source_data objects
    """


    # ------------------------------------------------

    def __init__( self ):

        self.sources = {}


    # ------------------------------------------------

    def add_database_connection(self, db:DBConnection):
        """
        connect to database
        """
        self.db = db

        if not self.db.schema_exists( 'sources' ):
            raise Exception( " schema sources does not exist " )

        if not self.db.table_exists( 'sources' , 'data_sources' ):
            raise Exception( " table data_sources does not exist " )

        query = f" select * from sources.data_sources "
        cursor = self.db.get_sql_cursor(query)

        for row in cursor.fetchall():

            data_source = DataSource( row[0] , row[1] , row[2] , row[3] , row[4] )

            self.sources[ row[0] ] = data_source

        cursor.close()


    def add_data_source( self, schema_name, source_name, source_version, source_description, source_directory ):
        """
        Add a DataSource object
        :param schema_name:
        :param source_name:
        :param source_version:
        :param source_description:
        :param source_directory:
        :return:
        """

        if not self.data_source_exits( schema_name ):
            data_source = DataSource( schema_name, source_name, source_version, source_description, source_directory )

            self.sources[ schema_name ] = data_source

            query = f" insert into sources.data_sources values( '{schema_name}' , '{source_name}' , " \
                    f" '{source_version}' , '{source_description}' , '{source_directory}' )"
            self.db.execute_query( query )



    # ------------------------------------------------

    def delete_data_source( self, schema_name ):

        if self.data_source_exits( schema_name ):

            del self.sources[ schema_name ]


    # ------------------------------------------------

    def get_sources( self ):

        return self.sources.values();

    # ------------------------------------------------

    def source_count( self ):

        return len( self.sources )

    # ------------------------------------------------

    def data_source_exits( self, schema_name ):
        """
        check if the schema exits
        :param schema_name:
        """

        return schema_name in self.sources;


    # ------------------------------------------------


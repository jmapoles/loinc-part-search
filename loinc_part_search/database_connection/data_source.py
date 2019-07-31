# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class DataSource:
    """
    Represents one row of the data_sources table
    add date of release? year?
    """


    # ------------------------------------------------

    def __init__(self, schema_name , source_name , source_version , source_description , source_directory ):
        """

        :param schema_name: name used in the db for this schema, loinc_264
        :param source_name: name of the source, loinc
        :param source_version: version of this release, 2.64
        :param source_description: description of source, containing dates etc.
        :param source_directory: directory where the source files are stored
        """

        self.schema_name = schema_name
        self.source_name = source_name
        self.source_version = source_version
        self.source_description = source_description
        self.source_directory = source_directory


    # ------------------------------------------------

    def get_schema_name( self ): return self.schema_name
    def get_source_name( self ): return self.source_name
    def get_source_version( self ): return self.source_version
    def get_source_description( self ): return self.source_description
    def get_source_directory( self ): return self.source_directory


    # ------------------------------------------------



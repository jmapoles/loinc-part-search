import configparser
from loinc_part_search.database_connection.db_queries import QueryLOINC


# --------------------------------------------------------
class LoadLOINCConfigurationFile:

    # required in the config file
    # data_source is the section name and the rest entries
    data_source = 'data_source'
    schema = 'schema'
    source = 'source'
    version = 'version'
    description = 'description'
    source_directory = 'source_directory'

    # attributes_type_definitions is the section name of new attribute definitions
    attribute_type_definitions = 'attribute_type_definitions'


    def __init__(self, type , server, user_name, password, database , schema , file_path ):

        self.db_conn = QueryLOINC( type , server, user_name, password, database , schema )
        self.db_conn.create_connection()

        # reads the config file
        # optionxform = str keeps key case as in file not convert to lowercase
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read( file_path )

        # data source
        if LoadLOINCConfigurationFile.data_source not in parser.sections():
            raise Exception( " data source not in config file " )

        self.check_for_data_source_keys( parser[ LoadLOINCConfigurationFile.data_source ] )

        schema_value = parser.get( LoadLOINCConfigurationFile.data_source, LoadLOINCConfigurationFile.schema )
        source_value = parser.get( LoadLOINCConfigurationFile.data_source, LoadLOINCConfigurationFile.source )
        version_value = parser.get( LoadLOINCConfigurationFile.data_source, LoadLOINCConfigurationFile.version )
        description_value = parser.get( LoadLOINCConfigurationFile.data_source, \
                                        LoadLOINCConfigurationFile.description )
        source_directory_value = parser.get( LoadLOINCConfigurationFile.data_source, \
                                             LoadLOINCConfigurationFile.source_directory )

        self.db_conn.data_sources.add_data_source( schema_value , source_value , version_value , description_value , \
                                      source_directory_value )

        # attribute type definitions
        if LoadLOINCConfigurationFile.attribute_type_definitions in parser.sections():

           for key , value in parser[ LoadLOINCConfigurationFile.attribute_type_definitions ].items():

               self.db_conn.attribute_type_definitions.add_attribute_type_definition( key, value )


    def check_for_data_source_keys( self , dict ):

        for entry in [ LoadLOINCConfigurationFile.schema , \
                       LoadLOINCConfigurationFile.source , \
                       LoadLOINCConfigurationFile.version , \
                       LoadLOINCConfigurationFile.description , \
                       LoadLOINCConfigurationFile.source_directory ]:

            if entry not in dict :

                raise Exception( f" {entry} not in config file " )



    # --------------------------------------------------------
    # --------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def main():

    config_file = "C:\Development\DataFiles\LOINC\LOINC_265\loinc_265.cfg"
    LoadLOINCConfigurationFile( "postgres", "localhost", "postgres", "JANN1qwe1!", "USMedicalCodes", "loinc_265", config_file )


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':

    main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

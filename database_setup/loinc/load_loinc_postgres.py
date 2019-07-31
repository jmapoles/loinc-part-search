import csv
import time
import sys

from loinc_part_search.database_connection.db_connection import DBConnection
from database_setup.loinc.create_loinc_schema import CreatePostgresSchema
from database_setup.loinc.load_loinc_config_file import LoadLOINCConfigurationFile
from loinc_part_search.database_connection.data_sources import DataSources
from loinc_part_search.database_connection.attribute_type_definitions import AttributeTypeDefinitions

# --------------------------------------------------------
class LoadLOINC:


    def __init__(self, type , server, user_name, password, database , schema ):

        self.conn = DBConnection( type , server, user_name, password, database )

        # cache of loinc code to object id
        self.codesToIdCache = {}

        # keeps track of id values during load
        self.id = 0

        self.schema = schema

        self.data_sources:DataSources = DataSources()
        self.data_sources.add_database_connection( self.conn )

        self.attribute_type_definitions:AttributeTypeDefinitions = AttributeTypeDefinitions()
        self.attribute_type_definitions.add_database_connection( self.conn )



        # mapping of columns to attribute names
        self.name_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Name' )

        self.loinc_code_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'LOINC Code' )
        self.loinc_part_code_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'LOINC Part Code' )
        self.loinc_component_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Component' )
        self.loinc_property_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Property' )
        self.loinc_time_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Time Aspect' )
        self.loinc_system_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'System' )
        self.loinc_scale_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Scale Type' )
        self.loinc_method_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Method Type' )
        self.loinc_class_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Class' )
        self.loinc_status_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Status' )
        self.loinc_class_type_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Class Type' )
        self.loinc_long_name_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'LOINC Long Name' )
        self.loinc_rank_id = self.attribute_type_definitions.get_attribute_type_definition_id( 'Common Rank' )


    # --------------------------------------------------------
    # --------------------------------------------------------

    def save_loinc_attribute(self, obj_id, attribute_id, attribute_value, preferred, cursor):

        attribute_value = DBConnection.escape_field(attribute_value)

        query = f" insert into {self.schema}.code_attributes values( {obj_id} , {attribute_id} , '{attribute_value}' , '{preferred}' )"
        cursor.execute(query)


    # --------------------------------------------------------

    def load_loinc_table(self, file_path):

        def save_loinc_code(obj_id, loinc_code, cursor):

            query = f" insert into {self.schema}.codes values( {obj_id} , {self.loinc_code_id} , '{loinc_code}' )"
            cursor.execute(query)

        load_cursor = self.conn.get_cursor()


        print(time.time())
        with open(file_path, "r", newline='', encoding='utf-8') as file:

            csv_reader = csv.reader(file)

            for row in csv_reader:

                # should not occur
                if row[0] in self.codesToIdCache:
                    continue

                print( row[0] , self.id )

                save_loinc_code(self.id, row[0], load_cursor)
                self.codesToIdCache[row[0]] = self.id

                zero = 'f'
                one = 't'


                self.save_loinc_attribute(self.id, self.loinc_component_id , row[1], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_property_id , row[2], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_time_id , row[3], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_system_id , row[4], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_scale_id , row[5], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_method_id , row[6], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_class_id , row[7], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_status_id , row[11], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_class_type_id , row[13], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.loinc_rank_id , row[36], zero, load_cursor)

                self.save_loinc_attribute(self.id, self.loinc_long_name_id , row[22], zero, load_cursor)
                self.save_loinc_attribute(self.id, self.name_id , row[28], one, load_cursor)

                self.id += 1

                if self.id % 10000 == 0:
                    self.conn.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.conn.commit()


        load_cursor.close()
        print(time.time())

    # --------------------------------------------------------

    def load_mah_table(self, file_path):

        def save_mah_code(obj_id, loinc_part_code, cursor):

            query = f" insert into {self.schema}.codes values( {obj_id} , {self.loinc_part_code_id} , '{loinc_part_code}' )"
            cursor.execute(query)

        load_cursor = self.conn.get_cursor()


        print(time.time())
        with open(file_path, "r", newline='', encoding='utf-8') as file:

            csv_reader = csv.reader(file)

            for row in csv_reader:

                # duplicates in file, multiple parents and LOINC codes
                if row[3] in self.codesToIdCache:
                    continue

                save_mah_code(self.id, row[3], load_cursor)
                self.codesToIdCache[row[3]] = self.id

                self.save_loinc_attribute(self.id, self.name_id , row[4], 't', load_cursor)

                self.id += 1

                if self.id % 5000 == 0:
                    self.conn.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.conn.commit()


        load_cursor.close()
        print(time.time())

    def load_hierarchy_table(self, file_path):

        def save_hierarchy_codes(parent_id, obj_id, cursor):

            query = f" insert into {self.schema}.code_hierarchy values( {parent_id} , {obj_id} )"
            cursor.execute(query)

        is_loaded = set()
        hierarchy_id = 0
        load_cursor = self.conn.get_cursor()


        print(time.time())
        with open(file_path, "r", newline='', encoding='utf-8') as file:

            csv_reader = csv.reader(file)

            for row in csv_reader:

                if row[2] == "":
                    pass
                elif row[2] not in self.codesToIdCache:
                    print("\n\nParentId" + row[2] + " not a known code\n\nexit\n")
                    sys.exit(1)

                if row[3] not in self.codesToIdCache:
                    print("\n\nID: " + row[3] + " not a known code\n\nexit\n")
                    sys.exit(1)

                code_id = self.codesToIdCache.get(row[3])

                # value -1 indicates no parents, top of hierarchy
                if row[2] == "":
                    parent_code_id = -1
                else:
                    parent_code_id = self.codesToIdCache.get(row[2])

                # screen for duplicates in the file
                if (parent_code_id, code_id) in is_loaded:
                    continue

                is_loaded.add((parent_code_id, code_id))

                save_hierarchy_codes(parent_code_id, code_id, load_cursor)

                hierarchy_id += 1

                if hierarchy_id % 5000 == 0:
                    self.conn.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.conn.commit()


        load_cursor.close()
        print(time.time())

    # --------------------------------------------------------
    # --------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def main():

    # variable used to load each LOINC file
    load_type = 'postgres'
    server = 'localhost'
    user = 'postgres'
    passwd = 'JANN1qwe1!'
    database = 'USMedicalCodes'
    schema = 'loinc_265'
    config_file = None
    loinc_path = "C:\Development\DataFiles\LOINC\LOINC_265\loinc.csv"
    mah_path = "C:\Development\DataFiles\LOINC\LOINC_265\MultiAxialHierarchy.csv"


    # creates the loinc schema
    CreatePostgresSchema( load_type , server , user , passwd , database , schema )


    # load the config file if there is one
    # for LOINC there will rarely be a new file, unless a new field is created
    if config_file:
        LoadLOINCConfigurationFile( load_type , server , user , passwd , database , schema , config_file )


    # load the files
    loinc_connection = LoadLOINC( load_type , server , user , passwd , database , schema )

    loinc_connection.load_loinc_table(loinc_path)
    loinc_connection.load_mah_table(mah_path)
    loinc_connection.load_hierarchy_table(mah_path)


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

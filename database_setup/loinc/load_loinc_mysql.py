import csv
import time
import sys
from loinc_part_search.database_connection.db_connection import DBConnection
from loinc_part_search.loinc_objects.loinc_eav_constants import LOINCEAVConstants


# --------------------------------------------------------
class LoadLOINC(DBConnection):

    def __init__(self, type , server, user_name, password, database):

        self.mysql = DBConnection( type , server, user_name, password, database)

        # cache of loinc code to object id
        self.codesToIdCache = {}

        # keeps track of id values during load
        self.id = 0

    # --------------------------------------------------------
    # --------------------------------------------------------

    def save_loinc_attribute(self, obj_id, attribute_id, attribute_value, preferred, cursor):

        attribute_value = DBConnection.escape_field(attribute_value)

        query = f" insert into code_attributes values( {obj_id} , {attribute_id} , '{attribute_value}' , '{preferred}' )"
        if type == 'mysql':
            query = f" insert into code_attributes values( {obj_id} , {attribute_id} , '{attribute_value}' , {preferred} )"

        cursor.execute(query)


    # --------------------------------------------------------

    def load_loinc_table(self, file_path):

        def save_loinc_code(obj_id, loinc_code, cursor):

            query = f" insert into codes values( {obj_id} , {LOINCEAVConstants.loinc_code_definition} , '{loinc_code}' )"
            cursor.execute(query)

        load_cursor = self.mysql.get_cursor()

        # autocommit for mysql
        if type == 'mysql':
            load_cursor.execute(" set autocommit = 0 ")

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
                if type == 'mysql':
                    zero = 0
                    one = 1


                self.save_loinc_attribute(self.id, LOINCEAVConstants.component_definition, row[1], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.property_definition, row[2], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.time_aspect_definition, row[3], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.system_definition, row[4], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.scale_type_definition, row[5], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.method_type_definition, row[6], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.class_definition, row[7], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.status_definition, row[11], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.class_type_definition, row[13], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.common_rank_definition, row[36], zero, load_cursor)

                self.save_loinc_attribute(self.id, LOINCEAVConstants.short_name_definition, row[22], zero, load_cursor)
                self.save_loinc_attribute(self.id, LOINCEAVConstants.name_definition, row[28], one, load_cursor)

                self.id += 1

                if self.id % 10000 == 0:
                    self.mysql.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.mysql.commit()


        if type == 'mysql':
            load_cursor.execute(" set autocommit = 1 ")

        load_cursor.close()
        print(time.time())

    # --------------------------------------------------------

    def load_mah_table(self, file_path):

        def save_mah_code(obj_id, loinc_part_code, cursor):

            query = f" insert into codes values( {obj_id} , {LOINCEAVConstants.loinc_part_definition} , '{loinc_part_code}' )"
            cursor.execute(query)

        load_cursor = self.mysql.get_cursor()

        if type == 'mysql':
            load_cursor.execute(" set autocommit = 0 ")

        print(time.time())
        with open(file_path, "r", newline='', encoding='utf-8') as file:

            csv_reader = csv.reader(file)

            for row in csv_reader:

                # duplicates in file, multiple parents and LOINC codes
                if row[3] in self.codesToIdCache:
                    continue

                save_mah_code(self.id, row[3], load_cursor)
                self.codesToIdCache[row[3]] = self.id

                self.save_loinc_attribute(self.id, LOINCEAVConstants.name_definition, row[4], True, load_cursor)

                self.id += 1

                if self.id % 5000 == 0:
                    self.mysql.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.mysql.commit()

        if type == 'mysql':
            load_cursor.execute(" set autocommit = 1 ")

        load_cursor.close()
        print(time.time())

    def load_hierarchy_table(self, file_path):

        def save_hierarchy_codes(parent_id, obj_id, cursor):

            query = f" insert into code_hierarchy values( {parent_id} , {obj_id} )"
            cursor.execute(query)

        is_loaded = set()
        hierarchy_id = 0
        load_cursor = self.mysql.get_cursor()

        if type == 'mysql':
            load_cursor.execute(" set autocommit = 0 ")

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
                    self.mysql.commit()
                    print(str(self.id) + " " + str(time.time()))

                self.mysql.commit()

        if type == 'mysql':
            load_cursor.execute(" set autocommit = 1 ")

        load_cursor.close()
        print(time.time())

    # --------------------------------------------------------
    # --------------------------------------------------------


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def main():
    
    loinc_path = "C:\Development\DataFiles\LOINC\LOINC_264\loinc.csv"
    mah_path = "C:\Development\DataFiles\LOINC\LOINC_264\MultiAxialHierarchy.csv"
    source_path = "C:\Development\DataFiles\LOINC\LOINC_264\source.tx"
    attributes_path = "C:\Development\DataFiles\LOINC\LOINC_264\attributes.tx"

    loinc_connection = LoadLOINC( "postgres" , "localhost", "postgres", "JANN1qwe1!", "USMedicalCodes" )



    loinc_connection.load_loinc_table(loinc_path)
    loinc_connection.load_mah_table(mah_path)
    loinc_connection.load_hierarchy_table(mah_path)


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

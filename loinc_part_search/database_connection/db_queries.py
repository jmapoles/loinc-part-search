# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.database_connection.db_connection import DBConnection
from typing import Set
from loinc_part_search.database_connection.data_sources import DataSources
from loinc_part_search.database_connection.attribute_type_definitions import AttributeTypeDefinitions


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class QueryLOINC:
    """
    Query database
    """
    # --------------------------------------------------------

    def __init__(self, type , server, user_name, password, database , schema ):
        """
        :param server:
        :param user_name:
        :param password:
        :param database:

        This creates DB connection, can be expanded
            to take other connectors
        """

        self.type = type
        self.server = server
        self.user_name = user_name
        self.password = password
        self.database = database
        self.schema = schema

        self.query_db = None

    def create_connection(self):
        """
        connect to MySQLConnection
        """
        self.query_db = DBConnection(self.type,self.server, self.user_name, self.password, self.database )

        self.data_sources:DataSources = DataSources()
        self.data_sources.add_database_connection( self.query_db )

        self.attribute_type_definitions:AttributeTypeDefinitions = AttributeTypeDefinitions()
        self.attribute_type_definitions.add_database_connection( self.query_db )


    def change_schema( self, schema ):

        self.schema = schema


    # --------------------------------------------------------

    def get_obj_id_of_code_type(self, attribute_definition , code):
        """
        :param attribute_definition:
        :param code:
        :return: id(int) or None

        return the id of the loinc code
        """


        # get the codes table for the code
        query = f" select * from {self.schema}.codes where defining_value = '{code}' and " \
                f"   defining_id = {attribute_definition} "

        row = self.query_db.return_single_row( query )

        if row is None:
            return None

        return row[0]



    def obj_id_exists(self, obj_id):
        """
        :param obj_id:
        :return: boolean

        checks that obj_id is in the codes table
        """


        # get codes table for the obj_id
        query = f" select * from {self.schema}.codes where id = {obj_id} "

        row = self.query_db.return_single_row( query )

        if row is None:
            return False

        return True


    def get_defining_attributes_of_obj_id(self, obj_id):
        """
        :rtype:
        :param obj_id:
        :return: tuple

        query returns tuple from code: defining_id , defining_value
        """


        # get codes table for the obj_id
        query = f" select * from {self.schema}.codes where id = {obj_id} "

        row = self.query_db.return_single_row ( query )
        if row is None:
            return None

        return row[1] , row[2]


    def get_attributes_of_obj_id(self, obj_id ):
        """
        :param obj_id:
        :return: list of tuples

        return all attributes of the id
        """

        # get the returns code_attributes table
        query = f" select * from {self.schema}.code_attributes where id = {obj_id} "
        cursor = self.query_db.get_sql_cursor(query)

        attributes = []
        for row in cursor.fetchall():

            attributes.append( ( row[1] , row[2] , row[3] ) )

        cursor.close()

        return attributes


    # --------------------------------------------------------

    def get_parent_ids_of_obj_id(self, obj_id) -> Set:
        """
        :param obj_id:
        :return: set of object ids that are parents of obj_id

        collects the parents of a obj_id and returns the ids as a set
        """

        parents = set()

        query = f" select * from {self.schema}.code_hierarchy where id = {obj_id} "
        cursor = self.query_db.get_sql_cursor(query)

        for row in cursor.fetchall():
            parents.add(row[0])

        cursor.close()

        return parents


    def get_child_ids_of_obj_id(self, obj_id) -> Set:
        """
        :param obj_id:
        :return: set of object ids that are children of obj_id

        collects the children of a obj_id and returns the ids as a set
        """

        children = set()

        query = f" select * from {self.schema}.code_hierarchy where parent_id = {obj_id} "
        cursor = self.query_db.get_sql_cursor(query)

        for row in cursor.fetchall():
            children.add(row[1])

        cursor.close()

        return children


    # --------------------------------------------------------
    # --------------------------------------------------------

    def get_ancestor_ids_of_obj_id(self, obj_id):
        """
        :param obj_id:
        :return: set of all ancestors

        returns a set of all ancestors of obj_id or add to scratch table when to_scratch set to True
        """

        ancestors = set()


        query = ' WITH RECURSIVE cte (id) AS '
        query = query + ' ( '
        query = query + f' select parent_id from {self.schema}.code_hierarchy where id = {obj_id} and parent_id <> -1 '
        query = query + ' UNION ALL '
        query = query + f' select h.parent_id from {self.schema}.code_hierarchy h , cte c where h.id = c.id and h.parent_id <> -1 '
        query = query + ' ) '
        query = query + ' select distinct * from cte ;'
        cursor = self.query_db.get_sql_cursor(query)


        for row in cursor.fetchall():
            # added for testing duplicates filter in query
            if row[0] == -1:
                continue
            else:
                ancestors.add(row[0])

        cursor.close()

        return ancestors


    def get_ancestor_ids_of_obj_id_to_level(self, obj_id, level: int):
        """

        :param obj_id:
        :param level: maximum number to step up in the hierarchy
        :return: set of ancestors of obj_id

        returns a set of all the ancestors of obj_id add to scratch table when to_scratch set to True
        """

        ancestors = set()

        if level < 1:
            return ancestors

        if level == 1:
            return self.get_parent_ids_of_obj_id( obj_id )



        query = ' WITH RECURSIVE cte (id,ct) AS '
        query = query + ' ( '
        query = query + f' select parent_id , 1 from {self.schema}.code_hierarchy where id = {obj_id} and parent_id <> -1 '
        query = query + ' UNION ALL '
        query = query + f' select h.parent_id , c.ct + 1 from {self.schema}.code_hierarchy h , cte c '
        query = query + f'       where h.id = c.id and h.parent_id <> -1 and c.ct <= {level} '
        query = query + ' ) '
        query = query + ' select distinct id , ct from cte ; '
        cursor = self.query_db.get_sql_cursor(query)


        for row in cursor.fetchall():
            if row[1] > level:
                continue
            else:
                ancestors.add(row[0])


        cursor.close()

        return ancestors


    # --------------------------------------------------------

    def get_descendant_ids_of_id(self, obj_id) -> Set:
        """

        :param obj_id:
        :return: set of descendants of object id
        """
        descendants = set()

        query = " WITH RECURSIVE cte (id) AS "
        query = query + " ( "
        query = query + f" select id from {self.schema}.code_hierarchy where parent_id = {obj_id} "
        query = query + " UNION ALL "
        query = query + f" select h.id from {self.schema}.code_hierarchy h , cte c where h.parent_id = c.id "
        query = query + " ) "
        query = query + " select distinct * from cte ; "
        cursor = self.query_db.get_sql_cursor( query)

        for row in cursor.fetchall():
            descendants.add(row[0])

        cursor.close()

        return descendants


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

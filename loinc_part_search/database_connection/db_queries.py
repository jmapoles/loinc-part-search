# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

from loinc_part_search.database_connection.db_connection import DBConnection
from typing import Set

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class QueryLOINC:
    """
    Query MySQL database
    """
    # --------------------------------------------------------

    def __init__(self, type , server, user_name, password, database):
        """
        :param server:
        :param user_name:
        :param password:
        :param database:

        This creates the MySQL connection, could be expanded
            to take other connectors
        """

        self.type = type
        self.server = server
        self.user_name = user_name
        self.password = password
        self.database = database

        self.mysql = None

    def create_connection(self):
        """
        connect to MySQLConnection
        """
        self.mysql = DBConnection(self.type,self.server, self.user_name, self.password, self.database)



    # --------------------------------------------------------

    def get_obj_id_of_code_type(self, attribute_definition , code):
        """
        :param attribute_definition:
        :param code:
        :return: id(int) or None

        return the id of the loinc code
        """


        # get the codes table for the code
        query = f" select * from codes where definingValue = '{code}' and " \
                f"   definingId = {attribute_definition} "

        row = self.mysql.return_single_row( query )

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
        query = f" select * from codes where id = {obj_id} "

        row = self.mysql.return_single_row( query )

        if row is None:
            return False

        return True


    def get_defining_attributes_of_obj_id(self, obj_id):
        """
        :rtype:
        :param obj_id:
        :return: tuple

        query returns row from code: id , attributeId , attributeValue
        a list is returned with attributeId and attributeValue
        """


        # get codes table for the obj_id
        query = f" select * from codes where id = {obj_id} "

        row = self.mysql.return_single_row ( query )
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
        query = f" select * from code_attributes where id = {obj_id} "
        cursor = self.mysql.get_sql_cursor(query)

        attributes = []
        for row in cursor.fetchall():

            attributes.append( ( row[1] , row[2] , row[3] ) )

        cursor.close()

        return attributes


    # --------------------------------------------------------

    def get_parent_ids_of_obj_id(self, obj_id) -> Set:
        """
        :param obj_id:
        :return: set of object ids that are parents of Obj_id

        collects the parents of a obj_id and returns their ids as a set
        """

        parents = set()

        query = f" select * from code_hierarchy where id = {obj_id} "
        cursor = self.mysql.get_sql_cursor(query)

        for row in cursor.fetchall():
            parents.add(row[0])

        cursor.close()

        return parents


    def get_child_ids_of_obj_id(self, obj_id) -> Set:
        """
        :param obj_id:
        :return: set of object ids that are children of Obj_id

        collects the children of a obj_id and returns their ids as a set
        """

        children = set()

        query = f" select * from code_hierarchy where parentId = {obj_id} "
        cursor = self.mysql.get_sql_cursor(query)

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
        query = query + f' select parentId from code_hierarchy where id = {obj_id} and parentId <> -1 '
        query = query + ' UNION ALL '
        query = query + ' select h.parentId from code_hierarchy h , cte c where h.id = c.id and h.parentId <> -1 '
        query = query + ' ) '
        query = query + ' select distinct * from cte ;'
        cursor = self.mysql.get_sql_cursor(query)


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
        query = query + f' select parentId , 1 from code_hierarchy where id = {obj_id} and parentId <> -1 '
        query = query + ' UNION ALL '
        query = query + ' select h.parentId , c.ct + 1 from code_hierarchy h , cte c '
        query = query + f'       where h.id = c.id and h.parentId <> -1 and c.ct <= {level} '
        query = query + ' ) '
        query = query + ' select distinct id , ct from cte ; '
        cursor = self.mysql.get_sql_cursor(query)


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
        query = query + f" select id from code_hierarchy where parentId = {obj_id} "
        query = query + " UNION ALL "
        query = query + " select h.id from code_hierarchy h , cte c where h.parentId = c.id "
        query = query + " ) "
        query = query + " select distinct * from cte ; "
        cursor = self.mysql.get_sql_cursor( query)

        for row in cursor.fetchall():
            descendants.add(row[0])

        cursor.close()

        return descendants


    # --------------------------------------------------------
    # --------------------------------------------------------




# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

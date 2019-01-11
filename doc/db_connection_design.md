# Data connection objects
Connection is done through two class:
1. MySQLConnection creates a connection to the MySQL db.
2. QueryMySQLLOINC queries the DB and returns variables, lists, and set of LOINC data.

These classes should not be instantiated themselves, rather use AccessLOINC to query and return EAV LOINC objects.


## Design

![](db_connection.png)

## MySQLConnection summary
1. __init__( self, server, user_name, password, database )
2. get_sql_cursor( self , sql_query )
3. execute_query(self, sql_insert )
4. commit(self)
5. return_single_row(self,query)
6. truncate_scratch_table1(self)
7. truncate_scratch_table2(self)
8. escape_field(text)

## QueryMySQLLOINC summary
1. __init__(self, server, user_name, password, database)
2. create_connection(self)
3. get_obj_id_of_loinc_code(self, loinc_code)
4. obj_id_exists(self, obj_id)
5. get_defining_attributes_of_obj_id(self, obj_id)
6. get_attributes_of_obj_id(self, obj_id )
7. get_parent_ids_of_obj_id(self, obj_id)
8. get_child_ids_of_obj_id(self, obj_id)
9. get_ancestor_ids_of_obj_id(self, obj_id )
10. get_ancestor_ids_of_obj_id_to_level(self, obj_id, level: int )
11. get_descendant_ids_of_id(self, obj_id)


## MySQLConnection in mysql_connection
1. Imports pymysql
2. __init__( self, server, user_name, password, database )
    1. calls pymysql.connect to create a connection
3. get_sql_cursor( self , sql_query )
    1. executes the query and return a cursor pointed to the resulting rows
4. execute_query(self, sql_insert )
    1. executes an insert and commits results
5. commit(self)
    1. wraps the pymysql commit
6. return_single_row(self,query)
    1. executes the query and returns the first row if it exists
    2. return None if the query returns None
7. truncate_scratch_table1(self)
    1. truncates scratch table 1
8. truncate_scratch_table2(self)
    1. truncates scratch table 2
9. escape_field(text)
    1. static method
    2. escapes a text field; the apostrophe ' changed to ''
## QueryMySQLLOINC in mysql_queries
1. imports
    1. MySQLConnection
    2. LOINCEAVConstants
2. __init__(self, server, user_name, password, database)
    1. creates the mysql variable but does not make the connection.
    2. connection is uses create_connection() to make mock testing easier
3. create_connection(self)
    1. connects to MySQLConnection 
4. get_obj_id_of_loinc_code(self, loinc_code)
    1. return the id of the loinc code
    2. if it does not exist return None
    3. query
    ```
        select * 
          from codes 
         where attributeValue = '{loinc_code}' 
           and attributeId = {attribute_definition}
     ```
5. obj_id_exists(self, obj_id)
    1. returns true if this id exists in DB
    2. query
    ```
        select * from codes where id = {obj_id}
     ```
6. get_defining_attributes_of_obj_id(self, obj_id)
    1. returns the defining attributes of an id from the codes table as a tuple
        1. the attribute definition as the LOINCEAVConstants.constant_names value
        2. the attribute value
    2. if it does not exist a None is returned
    3. query
    ```
        select * from codes where id = {obj_id}
    ```
7. get_attributes_of_obj_id(self, obj_id )
    1. returns all attributes of the id as a list of tuples
        1. the attribute definition as the LOINCEAVConstants.constant_names value
        2. the attribute value
        3. preferred flag
    2. query
    ```
        select * from code_attributes where id = {obj_id}
    ```
8. get_parent_ids_of_obj_id(self, obj_id)
    1. returns a set of the ids parents
    2. query
    ```
        select * from code_hierarchy where id = {obj_id}
    ```
9. get_child_ids_of_obj_id(self, obj_id)
    1. returns a set of the ids children
    2. query
    ```
        select * from code_hierarchy where parentId = {obj_id}
    ```
10. get_ancestor_ids_of_obj_id(self, obj_id )
    1. returns ancestors of the id as a set
    2. a recurse query
    3. query
    ```
        select parentId 
          from code_hierarchy where id = {obj_id} 
           and parentId <> -1 
         UNION ALL
         select h.parentId 
           from code_hierarchy h , cte c 
          where h.id = c.id 
            and h.parentId <> -1
    ```
11. get_ancestor_ids_of_obj_id_to_level(self, obj_id, level: int )
    1. returns ancestors of the id as a set
    2. ancestors must be within a set number of step, the level variable, from the id
    3. a recursive query 
    4. query
    ```
        select parentId , 1 
          from code_hierarchy 
         where id = {obj_id}
           and parentId <> -1
        UNION ALL
        select h.parentId , c.ct + 1 
          from code_hierarchy h , cte c '
         where h.id = c.id 
           and h.parentId <> -1 
           and c.ct <= {level}
    ```
12. get_descendant_ids_of_id(self, obj_id)
    1. returns all descendants of the id as a set
    2. a recursive query
    3. query
    ```
        select id 
          from code_hierarchy 
         where parentId = {obj_id}
        UNION ALL
        select h.id 
          from code_hierarchy h , cte c 
         where h.parentId = c.id 
    ```

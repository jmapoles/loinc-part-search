# Data connection objects<br>
Connection is done through two class:<br>
1. DBConnection creates a connection to the LOINC db.<br>
   1. Two databases are supported MySQL and Postgres
2. QueryLOINC queries the DB and returns variables, lists, and sets of LOINC data.<br>

These classes should not be instantiated themselves, rather use AccessLOINC to query and return EAV LOINC objects.<br>


## Design

![](db_connection.png)

## DBConnection summary
1. __init__( self, type, server, user_name, password, database )
2. get_cursor( self )
3. get_sql_cursor( self , sql_query )
4. execute_query(self, sql_insert )
5. commit(self)
6. return_single_row(self,query)
7. escape_field(text)

## QueryLOINC summary
1. __init__(self, type , server, user_name, password, database)
2. create_connection(self)
3. get_obj_id_of_code_type(self, attribute_definition , code )
4. obj_id_exists(self, obj_id)
5. get_defining_attributes_of_obj_id(self, obj_id)
6. get_attributes_of_obj_id(self, obj_id )
7. get_parent_ids_of_obj_id(self, obj_id)
8. get_child_ids_of_obj_id(self, obj_id)
9. get_ancestor_ids_of_obj_id(self, obj_id )
10. get_ancestor_ids_of_obj_id_to_level(self, obj_id, level: int )
11. get_descendant_ids_of_id(self, obj_id)


## DBConnection in db_connection
1. Imports 
    1. pymysql
    2. psycopg2
2. __init__( self, type , server, user_name, password, database )
    1. Value of type can be 'mysql' or 'postgres'
    2. Create a connection based on type.
3. get_cursor( self ):
    1. returns a cursor from the connection object. 
4. get_sql_cursor( self , sql_query )
    1. executes the query and return a cursor pointed to the resulting rows
5. execute_query(self, sql_insert )
    1. executes an insert and commits results
6. commit(self)
    1. wraps the commit method
7. return_single_row(self,query)
    1. executes the query and returns the first row if it exists
    2. return None if the query returns None
8. escape_field(text)
    1. static method
    2. escapes a text field; the apostrophe ' changed to ''

## QueryLOINC in mysql_queries
1. imports
    1. DBConnection
    2. Set
2. __init__(self, type , server, user_name, password, database)
    1. creates the query_db variable but does not make the connection.
    2. connection is uses create_connection() to make mock testing easier
3. create_connection(self)
    1. connects to DBConnection 
4. get_obj_id_of_code_type(self, attribute_definition , code)
    1. return the id of the code
    2. if it does not exist return None
    3. query
    ```
        select * 
          from codes 
         where attribute_value = '{code}' 
           and attribute_id = {attribute_definition}
     ```
5. obj_id_exists(self, obj_id)
    1. returns true if this id exists in DB
    2. query
    ```
        select * from codes where id = {obj_id}
     ```
6. get_defining_attributes_of_obj_id(self, obj_id)
    1. returns the defining attributes of an id from the codes table as a tuple
        1. the defining definition as the LOINCEAVConstants.constant_names value
        2. the defining value
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
    1. returns a set of the id's parents
    2. query
    ```
        select * from code_hierarchy where id = {obj_id}
    ```
9. get_child_ids_of_obj_id(self, obj_id)
    1. returns a set of the id's children
    2. query
    ```
        select * from code_hierarchy where parent_id = {obj_id}
    ```
10. get_ancestor_ids_of_obj_id(self, obj_id )
    1. returns ancestors of the id as a set
    2. a recurse query
    3. query
    ```
        select parent_id 
          from code_hierarchy where id = {obj_id} 
           and parent_id <> -1 
         UNION ALL
         select h.parent_id 
           from code_hierarchy h , cte c 
          where h.id = c.id 
            and h.parent_id <> -1
    ```
11. get_ancestor_ids_of_obj_id_to_level(self, obj_id, level: int )
    1. returns ancestors of the id as a set
    2. ancestors must be within a set number of step, the level variable, from the id
    3. a recursive query 
    4. query
    ```
        select parent_id , 1 
          from code_hierarchy 
         where id = {obj_id}
           and parent_id <> -1
        UNION ALL
        select h.parent_id , c.ct + 1 
          from code_hierarchy h , cte c '
         where h.id = c.id 
           and h.parent_id <> -1 
           and c.ct <= {level}
    ```
12. get_descendant_ids_of_id(self, obj_id)
    1. returns all descendants of the id as a set
    2. a recursive query
    3. query
    ```
        select id 
          from code_hierarchy 
         where parent_id = {obj_id}
        UNION ALL
        select h.id 
          from code_hierarchy h , cte c 
         where h.parent_id = c.id 
    ```

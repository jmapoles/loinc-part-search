# Data connection objects

This is a stack of four classes that use QueryLOINC to access the LOINC DB.  
Returns are as LOINC EAV objects. AccessLOINC created using:

```
access_loinc = AccessLOINC ( "localhost", "root", "<password>", "loinc" )
access_loinc.make_connection()
```



## Design

![Access LOINC](access_loinc.png)

## AccessLOINC summary
1. get_descendants_obj_of_id_as_map(self, obj_id):

## AccessLOINCHierarchy summary
1. get_parent_obj_of_id(self, obj_id)
2. get_child_obj_of_id(self, obj_id)
3. get_ancestors_obj_of_id(self, obj_id)
4. get_ancestors_obj_of_id_to_level(self,obj_id,level)
5. get_descendants_obj_of_id(self, obj_id)
6. add_obj_to_list(self,list_of_id)

## AccessLOINCObj summary
1. __init__(self, server, user_name, password, database):
2. get_eav_obj_of_id(self, obj_id):
3. get_eav_obj_of_code(self, loinc_code ):
4. def get_eav_obj_of_part_code(self, obj_id ):

## AccessLOINCConnection summary
1. __init__(self, type, server, user_name, password, database):
2. get_obj_id_of_code_type(self, loinc_code ):
3. object_id_exists(self, obj_id ):
4. get_attributes_of_obj_id(self,obj_id):
5. get_defining_attributes_of_obj_id(self,obj_id):
6. get_parent_ids_of_obj_id(self, obj_id ):
7. get_child_ids_of_obj_id(self,obj_id):
8. get_ancestor_ids_of_obj_id(self,obj_id):
9. get_ancestor_ids_of_obj_id_to_level(self,obj_id):
10. get_descendant_ids_of_id(self,obj_id):



## AccessLOINC in access_loinc
1. imports EAVMap and extends AccessLOINCHierarchy
2. get_descendants_obj_of_id_as_map(self, obj_id):
    1. Takes an object id.
    2. If the object id exists the method returns a map of the object and all descendants.

## AccessLOINCHierarchy in access_loinc_hierarchy
1. extends AccessLOINCObj
2. get_parent_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all parent objects of the obj_id.
3. get_child_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all child objects of the obj_id.
4. get_ancestors_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all ancestor objects  of the obj_id.
5. get_ancestors_obj_of_id_to_level(self,obj_id,level)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all ancestor objects of the obj_id up to the level defined by the integer level.
    3. In the case of a single parent hierarchy this would be the number of steps up the LOINC Part code tree. In the case of a multi-parent hierarchy all ancestors that can be found within level steps are included.  There may be ancestors included in the list that have a path that is longer than level steps.
6. get_descendants_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all descendant objects of the obj_id.


## AccessLOINCObj in access_loinc_eav_object
1. Imports EAVObject, LOINCEAVConstants, and extends AccessLOINCConnection
2. get_eav_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exits the method returns the EAV object associated with the id.
    3. The defining attribute, attributes, and parent and children are added.
3. get_eav_obj_of_code(self, loinc_code )
    1. Takes a LOINC code.
    2. Returns get_eav_obj_of_id
4. get_eav_obj_of_part_code(self, obj_id )
    1. Takes a LOINC part code
    2. Returns get_eav_obj_of_id

## AccessLOINCConnection in access_loinc_connection
1. Imports QueryLOINC and EAVObject
2. __init__(self, type, server, user_name, password, database)
    1. Takes the DB parameters.
    2. Type can be 'mysql' or 'postgres' depending on the db type being used.
3. make_connection(self)
    1. Creates the DB connection.
4. get_eav_obj_of_id(self, obj_id)
   1. Wraps QueryLOINC call get_obj_id_of_code_type
5. obj_id_exists(self, obj_id)
   1. Wraps QueryLOINC call obj_id_exists
6. get_attributes_of_obj_id(self, loinc_code )
    1. Wraps QueryLOINC call get_attributes_of_obj_id
7. def get_defining_attributes_of_obj_id(self, obj_id )
    1. Wraps QueryLOINC call get_defining_attributes_of_obj_id
8. get_parent_ids_of_obj_id(self, obj_id )
    1. Wraps QueryLOINC call get_parent_ids_of_obj_id
9. get_child_ids_of_obj_id(self, loinc_code )
    1. Wraps QueryLOINC call get_child_ids_of_obj_id
10. get_ancestor_ids_of_obj_id(self, obj_id )
    1. Wraps QueryLOINC call get_ancestor_ids_of_obj_id
11. get_ancestor_ids_of_obj_id_to_level(self,obj_id)
    1. Wraps QueryLOINC call get_ancestor_ids_of_obj_id_to_level
12. get_descendant_ids_of_id(self,obj_id)
    1. Wraps QueryLOINC call get_descendant_ids_of_id
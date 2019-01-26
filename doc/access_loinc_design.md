# Data connection objects

This is a stack of three classes that use QueryMySQLLOINC to access the LOINC DB.  
Returns are LOINC EAV objects. AccessLOINC created using:

```
access_loinc = AccessLOINC ( "localhost", "root", "<password>", "loinc" )
access_loinc.make_connection()
```



## Design

![](access_loinc.png)

## AccessLOINC summary
1. get_descendants_obj_of_id_as_map(self, obj_id):

## AccessLOINCHiearchy summary
1. get_parent_obj_of_id(self, obj_id)
2. get_child_obj_of_id(self, obj_id)
3. get_ancestors_obj_of_id(self, obj_id)
4. get_ancestors_obj_of_id_to_level(self,obj_id,level)
5. get_descendants_obj_of_id(self, obj_id)
6. get_eav_ancestors_of_obj_id(self, obj_id)
7. get_eav_ancestors_of_obj_id_to_level(self, obj_id,level)
8. get_eav_descendant_of_obj_id(self, obj_id)

## AccessLOINCObj summary
1. __init__(self, server, user_name, password, database):
2. get_eav_obj_of_id(self, obj_id):
3. get_eav_obj_of_code(self, loinc_code ):
4. def get_eav_children_of_obj_id(self, obj_id ):
5. get_eav_parents_of_obj_id(self, obj_id ):
6. get_eav_obj_id_of_loinc_code(self, loinc_code ):
7. object_id_exists(self, obj_id ):
8. get_eav_defining_attributes_of_obj_id(self,obj_id):
9. get_eav_attributes_of_obj_id(self,obj_id):


## AccessLOINC in access_loinc
1. imports EAVMap and extends AccessLOINCHiearchy
2. get_descendants_obj_of_id_as_map(self, obj_id):
    1. Takes an object id.
    2. If this exists the method returns a map of the object and all descendants.

## AccessLOINCHiearchy in access_loinc_hierarchy
1. extends AccessLOINCHiearchy
2. get_parent_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all parents of the object.
3. get_child_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all children of the object.
4. get_ancestors_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all ancestors of the object.
5. get_ancestors_obj_of_id_to_level(self,obj_id,level)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all ancestors of the object up to the level defined by the integer level.
    3. In the case of a single parent hierarchy this would be the number of steps up the LOINC Part code tree. In the case of a multi-parent hierarchy all ancestors that can be found within level steps are included.  There may be ancestors included in the list that have a path that is longer than level steps.
6. get_descendants_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exists the method returns a list of all descendants of the object.
7. get_eav_ancestors_of_obj_id(self, obj_id)
    1. Wraps QueryMySQLLOINC call get_ancestor_ids_of_obj_id
8. get_eav_ancestors_of_obj_id_to_level(self, obj_id,level)
    1. Wraps QueryMySQLLOINC call get_eav_ancestors_of_obj_id_to_level
9. get_eav_descendant_of_obj_id(self, obj_id)
    1. Wraps QueryMySQLLOINC call get_eav_descendant_of_obj_id

## AccessLOINCObj in access_loinc_eav_object
1. Imports QueryMySQLLOINC and EAVObject
2. __init__(self, server, user_name, password, database)
    1. Takes the DB parameters.
3. map_connection(self)
    1. Creates the DB connection.
4. get_eav_obj_of_id(self, obj_id)
    1. Takes an object id.
    2. If the object id exits the method returns the EAV object associated with the id.
    3. The defining attribute, attributes, and parent and children are added.
5. get_eav_obj_of_code(self, loinc_code )
    1. Takes a LOINC code.
    2. Returns get_eav_obj_of_id
6. def get_eav_children_of_obj_id(self, obj_id )
    1. Wraps QueryMySQLLOINC call get_eav_children_of_obj_id
7. get_eav_parents_of_obj_id(self, obj_id )
    1. Wraps QueryMySQLLOINC call get_eav_parents_of_obj_id
8. get_eav_obj_id_of_loinc_code(self, loinc_code )
    1. Wraps QueryMySQLLOINC call get_eav_obj_id_of_loinc_code
9. object_id_exists(self, obj_id )
    1. Wraps QueryMySQLLOINC call object_id_exists
10. get_eav_defining_attributes_of_obj_id(self,obj_id)
    1. Wraps QueryMySQLLOINC call get_eav_defining_attributes_of_obj_id
11. get_eav_attributes_of_obj_id(self,obj_id)
    1. Wraps QueryMySQLLOINC call get_eav_attributes_of_obj_id



# EAV Object Design

The EAVObject is the data object used within scrips to store LOINC data returned from the database.  EAVMap stores a set of EAVObjects in a dictionary using the object id as the key. 

An object has a set of internal variables that describe the object.
* The object id is an internal unique variable (int) derived from the database. It is use as the primary key of the object with the database and links the row in the codes table to the other tables.
* The defining attribute and defining value are a unique pair within the database.  They are derived from the data-set, e.g. LOINC Code and a LOINC code value. These values are attributes but are stored in the codes table.
* All other attributes are stored as a dictionary.  The attribute definition is the key and attribute value is the value.
  * Currently each attribute definition references a single value.  If this variable is changed to a list then an attribute may have multiple values.
  * Attributes have a type of value, name, or reference.
     * values are attributes of the object and are strings varchar(1000)
     * names are used to name the object and are strings varchar(1000)
     * references are pointers to other objects and are integers
* parents and children are sets of integers. Integers are pointers to other objects and represent the parents or children in the hierarchy.
* The preferred attribute is an integer indicating the attribute definition that is the preferred name of the object.
  
Because objects contain a copy of their parents and children object id an EAVMap can be used to navigate a part of or the entire LOINC hierarchy. 

Generally objects are pulled from the database and will have an object id. Parents and children stored in the object will be references to objects in the database. But, objects can be created independently of the database and in those cases objects do not need to have an object id, and values stored in the parent and children set may not reference valid object.

## Design

![](eav_object.png)

## EAVObject summary
1. __init__(self, obj_id=None)
2. set_obj_id(self, obj_id)
3. add_parent(self, parent_id)
4. get_parents(self)
5. add_child(self, child_id)
6. get_children(self)
7. add_attribute(self, attribute_definition, attribute_value)
8. get_defining_attribute(self)
9. set_defining_attribute(self, attribute_definition, attribute_value)
10. get_preferred_attribute_value(self)
11. set_attribute_as_preferred(self, preferred_id)
12. get_preferred_id(self)
13. is_preferred(self, preferred_id)
14. display(self,level=5)
15. name_and_code_str(self)

## EAVMap summary
1. __init__(self)
2. add(self, obj_id, obj: EAVObject)
3. get_eav_object(self, obj_id)
4. has_obj_id(self, obj_id)
5. get_keys(self)
6. clear(self)
7. clear_obj_id(self, obj_id)
8. refactor_parent_child(self)
9. display_as_hierarchy(self)


## EAVObject in eav_objects
1. imports LOINCEAVConstants
2. __init__(self, obj_id=None)
    1. Initialize the object.
    2. If an id is provided it is stored as the object id.
3. set_obj_id(self, obj_id)
    1. Set the obj_id variable.
4. get_obj_id(self)
    2. Gets the obj_id variable
5. add_parent(self, parent_id)
    1. Adds the parent_id value to the parents set
6. get_parents(self)
    1. Gets the parents set
7. add_child(self, child_id)
    1. Adds the child_id value to the parents set 
8. get_children(self)
    1. Gets the children set.
9. add_attribute(self, attribute_definition, attribute_value)
    1. Adds the attribute definition and value to the
10. get_attributes(self)
    1. Return the attributes dictionary.

11. get_defining_attribute(self)
    1. Return the defining attribute tuple.
12. set_defining_attribute(self, attribute_definition, attribute_value)
    1. Add the definition and value as the defining attribute tuple.
13. get_preferred_id_value(self)
    1. If the preferred id is set and is a key in the attributes dictionary, return the value in the dictionary for the preferred id as a key.
14. set_attribute_as_preferred(self, preferred_id)
    1. Set the preferred id.
15. get_preferred_id(self)
    1. Return the preferred id.
16. is_preferred(self, preferred_id)
    1. Return False if the preferred id is not set.
    2. Return False if the preferred id is set but does not match the input value.
    3. Return True if the preferred id is set and matches the input value.
17. display(self,level=5)
    1. Displays information about the object depending on the level value.
    2. The display always prints the defining attribute, preferred attribute value, and the object id.
    3. If level is greater than 0 a list of attribute definitions and values is printed.
    4. If level is greater that 1 a list of parents is printed.
    5. if level is greater than 2 a list of children is printed.
18. name_and_code_str(self)
    1. Prints a one line summary of the object.
    2. [ object-id ], { defining attribute: defining value}: preferred attribute value

## EAVMap in eav_objects
1. imports LOINCEAVConstants
2. __init__(self)
    1. Initializes the map dictionary
3. add(self, obj_id, obj: EAVObject)
    1. Adds an object to the map using the object id as a key.
4. get_eav_object(self, obj_id)
    1. If the object id is a key in the map the object is returned.
    2. If the object id is not a key in the map then None is returned.
5. has_obj_id(self, obj_id)
    1. If the object id is a key in the map return True.
    2. If the object id is not a key in the map return False.
6. get_keys(self)
    1. Return the keys of the map as a list.
7. clear(self)
    1. Clear the entire map.
8. clear_obj_id(self, obj_id)
    1. Remove the object id from the map.
9. refactor_parent_child(self)
    1. All object in the map are reviewed.  Insures that parents of objects have that object listed as a child, and insures that children of an object have the object listed as a parent.
10. display_as_hierarchy(self)
    1. Displays a list of all objects in the map.
    2. Objects are displayed starting with objects without parents or parents that are not in the map.  
        1. All descendants are the printed "tabbed" in two spaces for each level below.
    3. All objects not printed are finally printed without a tab.



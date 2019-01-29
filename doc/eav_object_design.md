# EAV Object Design

The EAVObject is the data object used within scrips to store LOINC data returned from the database.  EAVMap stores a set of EAVObjects in a dictionary using the object id as the key. 

An object has a set of internal variables that describe the object.
* The object id is an internal, unique variable (int) derived from the database. It is use as the primary key of the object with the database and links the row in the codes table to the other tables.
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
1. __init__(self, obj_id=None , defining_definition=None , defining_value=None , attribute_definition=None , attribute_value=None )
2. set_obj_id(self, obj_id)
3. get_obj_id( self )
4. clear_obj_id( self )
5. add_parent(self, parent_id)
6. get_parents(self)
7. clear_parents(self)
8. add_child(self, child_id)
9. get_children(self)
10. clear_children(self)
11. add_attribute(self, attribute_definition, attribute_value, preferred=None)
12. add_attribute_tuple(self,attribute)
13. add_attributes(self,attributes:List)
14. get_attributes(self)
15. clear_attributes(self)
16. set_defining_attribute(self, attribute_definition, attribute_value)
17. get_defining_attribute(self)
18. clear_defining_attribute(self)
19. set_defining_attribute_and_name(self, defining_definition, defining_value , attribute_definition, attribute_value )
20. get_preferred_id_value(self)
21. set_attribute_as_preferred(self, preferred_id)
22. get_preferred_id(self)
23. is_preferred(self, preferred_id)
24. clear_preferred_id(self)
25. display(self,level=5)
26. name_and_code_str(self)

## EAVMap summary
1. __init__(self)
2. add(self, obj_id, obj: EAVObject)
3. get_eav_object(self, obj_id)
4. has_obj_id(self, obj_id)
5. get_keys(self)
6. clear(self)
7. clear_obj_id(self, obj_id)
8. size(self)
8. refactor_parent_child(self)
9. display_as_hierarchy(self)


## EAVObject in eav_objects
1. imports LOINCEAVConstants
2. __init__(self, obj_id=None , defining_definition=None , defining_value=None , attribute_definition=None , attribute_value=None)
    1. Initialize the object.
    2. If an id is provided it is stored as the object id.
    3. If defining_definition and defining_value are provided they are set.
    4. If attribute_definition and attribute_value are provide they are set as the preferred (name) attribute of the object.
3. set_obj_id(self, obj_id)
    1. Set the obj_id variable.
5. get_obj_id(self)
    2. Gets the obj_id variable
6. clear_obj_id(self)
    2. Clears the obj_id variable
7. add_parent(self, parent_id)
    1. Add the parent_id value to the parent set.
    2. parent_id must be an integer and greater than -1
8. get_parents(self)
    1. Get the parent set
9. clear_parents(self)
    1. Clear the parent set
10. add_child(self, child_id)
    1. Add the child_id value to the child set
    2. child_id must be an integer and greater than -1
11. get_children(self)
    1. Get the children set.
12. clear_children(self)
    1. Clear the children set.
13. add_attribute(self, attribute_definition, attribute_value, preferred=None )
    1. Adds the attribute definition and value to the attribute definition
14. add_attribute_tuple(self, attribute )
    1. Takes the attribute as a tuple and adds attribute[0] as definition and attribute[1] as value
15. get_attributes(self)
    1. Return the attributes dictionary.
16. clear_attributes(self)
    1. clears the attribute dictionary
17. set_defining_attribute(self, attribute_definition, attribute_value)
    1. Add the definition and value as the defining attribute tuple.
18. get_defining_attribute(self)
    1. Return the defining attribute tuple.
19. clear_defining_attribute(self)
    1. Clears the defining attribute tuple.
20. def set_defining_attribute_and_name(self, defining_definition, defining_value , attribute_definition, attribute_value )
    1. Helper method that adds defining attribute and an attribute to the object.  The attribute is usually the name.

21. get_preferred_id_value(self)
    1. Returns the preferred id.
22. set_attribute_as_preferred(self, preferred_id)
    1. If the id is a key the attributes dictionary, set the attribute as preferred.
23. get_preferred_id(self)
    1. Return the preferred id.
24. is_preferred(self, preferred_id)
    1. Return False if the preferred id is not set.
    2. Return False if the preferred id is set but does not match the input value.
    3. Return True if the preferred id is set and matches the input value.
25. clear_preferred_id(self)
    1. Clear the preferred id.
26. display(self,level=5)
    1. Displays information about the object depending on the level value.
    2. The display always prints the defining attribute, preferred attribute value, and the object id.
    3. If level is greater than 0 a list of attribute definitions and values is printed.
    4. If level is greater that 1 a list of parents is printed.
    5. if level is greater than 2 a list of children is printed.
27. name_and_code_str(self)
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
7. get_eav_objects(self)
    1. Return a list of all eav objects in the map.
8. clear(self)
    1. Clear the entire map.
9. clear_obj_id(self, obj_id)
    1. Remove the object id from the map.
11. size(self):
    1. return the length of the map.
12. refactor_parent_child(self)
    1. All object in the map are reviewed.  Insures that parents of objects have that object listed as a child, and insures that children of an object have the object listed as a parent.
13. display_as_hierarchy(self)
    1. Displays a list of all objects in the map.
    2. Objects are displayed starting with objects without parents or parents that are not in the map.  
        1. All descendants are the printed "tabbed" in two spaces for each level below.
    3. All objects not printed are finally printed without a tab.



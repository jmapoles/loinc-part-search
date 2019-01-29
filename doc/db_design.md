# DB design

The LOINC date is stored in four tables, codes, code_attributes, code_hierarchy, and attribute_definitions.<br>
The codes table lists all codes or objects.  Each code is unique and contains an external reference, code type and value and an internal reference (an unique integer). This integer, id, is used as the foreign key in the code_attributes and code_hierarchy tables.  The attribute_definitions table is a metadata table used to define the attributes used in codes and code_attributes.<br>

## ERD Design

![database erd](db_erd.png)<br>

## Tables
### codes: presents the individual codes derived from the LOINC files
1. id (int): primary key of the loinc object, sequential integer starting at 0. This is an internal value specific to this database.
    1. Each loinc code or loinc part code is represent in this table.
2. defining_id (int): id that represents the type of attribute, LOINC code or LOINC part code. These are defining attributes of the object, unique codes.
    1. This id is a foreign key from the attribute_definitions table that contains the name and type of the attribute.
3. defining_value (varchar(1000)): The value of the attribute.
    1. These are defining attributes and the combination of defining_id and defining_value are unique within the database.
### code_attributes: all attributes of the code excluding the defining attributes
1. id (int): foreign key from codes
2. attribute_id (int): id that represents the type of attribute.
    1. Attributes may be of type value, name, or reference. Values are internal attributes of the object such as unit of measure, etc. A name is an English string used to refer to the object.  A reference is a relationship to another object.  The code_hierarchy table captures a relationship explicitly, type-of or is-a.  
    2. This id is a foreign key from the attribute_definitions table that contains the name and type of the attribute.
3. attribute_value (varchar(1000)): The value of the attribute.
4. preferred (tinyint): Value is 0 for all attributes except one for each code. An attribute with value of '1' is the name of the object.
### code_hierarchy: models the parent-child relation of codes.  A code must have one or more parents, except for a top code which has no parents. No parents is indicated by a parent = -1.
1. parent_id (int): foreign key from the codes table
2. id (int): foreign key from the codes table
### attribute_definitions: This is the metadata of the DB.
1. attribute_id int(11):
2. attribute_name varchar(1000):
3. attribute_type enum('value','reference','name'):


| attribute_id | attribute_name    | attribute_type |
|:-------------|:------------------|:---------------|
| 1            | LOINC Code        | value          |
| 2            | LOINC Part Code   | value          |
| 3            | Component         | value          |
| 4            | Property          | value          |
| 5            | Time Aspect       | value          |
| 6            | System            | value          |
| 7            | Scale Type        | value          |
| 8            | Method Type       | value          |
| 9            | Class             | value          |
| 10           | Status            | value          |
| 11           | Class Type        | value          |
| 12           | Short Name        | name           |
| 13           | Long Name         | name           |
| 14           | Common Rank       | value          |






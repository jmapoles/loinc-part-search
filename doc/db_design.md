# DB design

The LOINC date is stored in four tables, codes, code_attributes, code_hierarchy, and attribute_definitions. The codes table is lists all codes, in this case LOINC codes and LOINC Part codes.  Each is indexed with an integer. This integer, id, is used as the foreign key in the code_attributes and code_hierarchy tables.  The primary attributes of the code are listed in the codes table.

## ERD Design

![database erd](db_erd.png)

## Tables
### codes: presents the individual codes derived from the LOINC files
1. id (int): primary key of the loinc object, sequential integer starting at 0
    1. Each loinc code or loinc part code is represent in this table.
2. definingId (int): id that represents the type of attribute. These are defining attributes of the object, unique codes.
    1. This id is a foreign key from the attribute_definitions table that contain the name and type of the attribute.
3. definingValue (varchar(1000)): The value of the attribute.  
    1.These are defining attributes and the combination of attributeId and attribute value are unique within the database.
### code_attributes: all attributes of the code excluding the defining attributes
1. id (int): foreign key from codes
2. attributeId (int): id that represents the type of attribute.
    1. This id is a foreign key from the attribute_definitions table that contain the name and type of the attribute.
3. attributeValue (varchar(1000)): The value of the attribute.  
4. preferred (tinyint): Value is 0 for all attributes except one for each code. Attribute with value 1 is the name of the code
### code_hierarchy: models the parent-child relation of codes.  A code must have one parent but may have many.  The top code has no parent indicated by a parent = -1.
1. parentId (int): foreign key from the codes table
2. id (int): foreign key from the codes table
### attribute_definitions: This is the metadata of the DB.  
1. attributeId int(11):
2. attributeName varchar(1000):
3. attributeType enum('value','reference','name'):


| attributeId | attributeName    | attributeType|
|:------------|:-----------------|:-------------|
| 1           | LOINC Code       | value        |
| 2           | LOINC Part Code  | value        |
| 3           | Component        | value        |
| 4           | Property         | value        |
| 5           | Time Aspect      | value        |
| 6           | System           | value        |
| 7           | Scale Type       | value        |
| 8           | Method Type      | value        |
| 9           | Class            | value        |
| 10          | Status           | value        |
| 11          | Class Type       | value        |
| 12          | Short Name       | name         |
| 13          | Long Name        | name         |
| 14          | Common Rank      | value        |





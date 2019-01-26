# DB design

The LOINC date is stored in four tables, codes, code_attributes, code_hierarchy, and attribute_definitions.<br>
The codes table is lists all codes or objects.  Each code is unique and contains an external reference, code type and value and an internal reference an unique integer. This integer, id, is used as the foreign key in the code_attributes and code_hierarchy tables.  The attribute_definitions table is a metadata table used to define the attributes used in codes and code_attributes.<br>

## ERD Design

![database erd](db_erd.png)<br>

## Tables
### codes: presents the individual codes derived from the LOINC files
1. id (int): primary key of the loinc object, sequential integer starting at 0
    1. Each loinc code or loinc part code is represent in this table.
2. definingid (int): id that represents the type of attribute. These are defining attributes of the object, unique codes.
    1. This id is a foreign key from the attribute_definitions table that contains the name and type of the attribute.
3. definingvalue (varchar(1000)): The value of the attribute.  
    1. These are defining attributes and the combination of attributeid and attribute value are unique within the database.
### code_attributes: all attributes of the code excluding the defining attributes
1. id (int): foreign key from codes
2. attributeid (int): id that represents the type of attribute.
    1. This id is a foreign key from the attribute_definitions table that contains the name and type of the attribute.
3. attributevalue (varchar(1000)): The value of the attribute.  
4. preferred (tinyint): Value is 0 for all attributes except one for each code. Attribute with value 1 is the name of the code
### code_hierarchy: models the parent-child relation of codes.  A code must have one parent but may have many.  The top code has no parent indicated by a parent = -1.
1. parentid (int): foreign key from the codes table
2. id (int): foreign key from the codes table
### attribute_definitions: This is the metadata of the DB.  
1. attributeid int(11):
2. attributeName varchar(1000):
3. attributeType enum('value','reference','name'):


| attributeid | attributeName    | attributeType|
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





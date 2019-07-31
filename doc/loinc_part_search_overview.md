# Overview loinc_part_search

This project builds LOINC codes into a hierarchy based on LOINC part codes.  Hierarchies are base on the multi-axial hierarchy table. This is a demonstration project.  Features will gradually be expanded.  Data is from LOINC 2.65. The database contains all data from the loinc.txt and multi-axial hierarchy table.<br>
The project is designed as a set of layers,
* database containing loinc data stored in a object–attribute–value model design,
  * MySQL and Postgres databases are supported,
* connection layer that connects to the database and queries that database,
* parsing layer that converts query data into objects.
* object layer that is used to contain parsed data.<br>
A small set of rest-api using Flask are available.<br>
Part of LOINC 2.65 has been configured as a demonstration project.  The database contains only the codes below Human Leukocyte Antigen, LOINC part code: LP56928-2.  This is to stay within the Heroku 10,000 Postgres row limit for a demonstration project.<br><br>

See https://loinc.org/license/ for Regenstrief license for the use and distribution of LOINC.<br>

Version=1.1.0<br>



# Documentation

1. [DB design](db_design.md): database table layout.

2. [DB connection design](db_connection_design.md):

3. [Access loinc design](access_loinc_design.md):

4. [EAV object design](eav_object_design.md): covers the design of the of data object containing loinc code data.

5. [web-api](web_api.md): web-api









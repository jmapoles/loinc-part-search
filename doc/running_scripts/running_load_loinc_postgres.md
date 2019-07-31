# Loading LOINC

1. If there is not existing database.
    1. create a new Postgres database
    2. run the script: data_setup/create_source_schema/sources_schema.sql
2. If there is an existing datbase
    1. run load data_setup/loinc/load_loinc_postgres.py
    2. edit the main of postgres.py
        1. load_type: usually 'postgres'
        2. server: usually 'localhost'
        3. user: the db user, currently 'postgres'
        4. passwd
        5. database: db name, currently 'USMedicalCodes'
        6. schema: name of the schema for this load: 'loinc_265'
        7. config_file: see description below
        8. loinc_path: location of the file 'loinc.csv'
        9. mah_path: location of the file 'MultiAxialHierarchy.csv'
3. config_file is required for a load.
    1. It has two sections: 'data_source' and 'attribute_type_definitions'
    2. 'data_source' is required
        1. schema: schema name, must match the value added to load_loinc_postgres.py schema variable
	    2. source: name of the dataset.  This should be the same for different versions
	    3. version: version of the release
	    4. description: short description of the dataset
	    5. source_directory: can be set to None, directory where source files are stored
    3. 'attribute_type_definitions' is optional and defines new metadata
        1. entries are key value pairs: name and attribute type.
        2. attribute type can be set to value, name, reference


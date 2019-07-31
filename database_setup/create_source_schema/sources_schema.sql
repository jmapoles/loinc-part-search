CREATE schema sources;

CREATE TYPE sources.attribute_types AS ENUM ( 'value' , 'reference' , 'name' );
CREATE TABLE sources.attribute_type_definitions ( attribute_id int not null ,
                                    	         attribute_name varchar(1000) not null ,
												 attribute_type sources.attribute_types ,
												 primary key( attribute_id ) );

insert into sources.attribute_type_definitions values( 1 , 'Name' , 'name' );


CREATE TABLE sources.data_sources ( schema_name varchar( 100 ) not null ,
                                    source_name varchar( 100 ) not null ,
                                    source_version varchar( 100 ) not null ,
                                    source_description varchar( 1000 ) not null ,
                                    source_directory varchar( 1000 ) null ,
                                    primary key( schema_name ) )
CREATE TABLE codes ( id int not null , definingId int not null , definingValue varchar(1000) not null , primary key( id ) );

CREATE TYPE attribute AS ENUM ('value' , 'reference' , 'name');
CREATE TABLE attribute_definitions ( attributeId int not null , attributeName varchar(1000) not null , attributeType attribute , primary key( attributeId ) );

CREATE TABLE code_hierarchy (  parentId int not null , id int not null );
create index co_parentidh_idx_id on code_hierarchy( id );
create index code_h_idx_parentid on code_hierarchy( parentId );

CREATE TABLE code_attributes ( id int not null , attributeId int not null , attributeValue varchar(1000) not null ,  preferred boolean );
create index code_att_id on code_attributes( id );

insert into attribute_definitions values( 1 , 'LOINC Code' , 'value' );
insert into attribute_definitions values( 2 , 'LOINC Part Code' , 'value' );
insert into attribute_definitions values( 3 , 'Component' , 'value' );
insert into attribute_definitions values( 4 , 'Property' , 'value' );
insert into attribute_definitions values( 5 , 'Time Aspect' , 'value' );
insert into attribute_definitions values( 6 , 'System' , 'value' );
insert into attribute_definitions values( 7 , 'Scale Type' , 'value' );
insert into attribute_definitions values( 8 , 'Method Type' , 'value' );
insert into attribute_definitions values( 9 , 'Class' , 'value' );
insert into attribute_definitions values( 10 , 'Status' , 'value' );
insert into attribute_definitions values( 11 , 'Class Type' , 'value' );
insert into attribute_definitions values( 12 , 'Short Name' , 'name' );
insert into attribute_definitions values( 13 , 'Long Name' , 'name' );
insert into attribute_definitions values( 14 , 'Common Rank' , 'value' );


drop table cytology_children;
drop table cytology_ids;
drop table cytology_hierarchy;
drop table cytology_codes;
drop table cytology_attributes;

-- ids of all descendants fo cytology
WITH RECURSIVE descendants( id )
	AS 
	( 
	select id from code_hierarchy where parentid = 113942
  	union all
    select c.id from code_hierarchy c , descendants d where c.parentid = d.id 
	)
select id into cytology_children from descendants
insert into cytology_children select 113942

select c.* into cytology_hierarchy
 from cytology_children d , code_hierarchy c , cytology_children d_p
 where d.id = c.id
   and c.parentid = d_p.id
insert into cytology_hierarchy
select -1 , 113942


select distinct id into cytology_ids from
(
select id FROM cytology_hierarchy 
union all
select parentid from cytology_hierarchy
) t

select c.* into cytology_codes from codes c , cytology_ids cy where c.id = cy.id
select a.* into cytology_attributes from code_attributes a , cytology_ids cy where a.id = cy.id

select count(*) from cytology_codes;
select count(*) from cytology_hierarchy;
select count(*) from cytology_attributes;












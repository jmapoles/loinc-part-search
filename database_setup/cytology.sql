select * from code_hierarchy c , code_attributes a
 where c.parentid = 113942 and c.id = a.id


WITH RECURSIVE descendants( id )
	AS
	(
	select id from code_hierarchy where parentid = 113942
  	union all
    select c.id from code_hierarchy c , descendants d where c.parentid = d.id
	)
select id into cytology_children from descendants
insert into cytology_children select 113942
--select * from descendants


select * from cytology_children




select c.* into cytology_hierarchy
 from cytology_children d , code_hierarchy c , cytology_children d_p
 where d.id = c.id
   and c.parentid = d_p.id
 order by c.parentid desc
insert into cytology_hierarchy
select -1 , 113942

select distinct id into cytology_ids from
(
select id FROM cytology_hierarchy
union all
select parentid from cytology_hierarchy
) t

select * from cytology_ids order by id


select c.* into cytology_codes from codes c , cytology_ids cy where c.id = cy.id
select a.* into cytology_attributes from code_attributes a , cytology_ids cy where a.id = cy.id

select * from loinc_demo.schemas.public.codes




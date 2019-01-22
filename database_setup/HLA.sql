
WITH RECURSIVE descendants( id )
	AS
	(
	select id from code_hierarchy where parentid = 11391105692
  	union all
    select c.id from code_hierarchy c , descendants d where c.parentid = d.id
	)
select id into HLA_children from descendants
insert into HLA_children select 110569
--select * from descendants


select * from HLA_children




select c.* into HLA_hierarchy
 from HLA_children d , code_hierarchy c , HLA_children d_p
 where d.id = c.id
   and c.parentid = d_p.id
 order by c.parentid desc
insert into HLA_hierarchy
select -1 , 110569

select distinct id into HLA_ids from
(
select id FROM HLA_hierarchy
union all
select parentid from HLA_hierarchy
) t

select * from HLA_ids order by id


select c.* into HLA_codes from codes c , HLA_ids cy where c.id = cy.id
select a.* into HLA_attributes from code_attributes a , HLA_ids cy where a.id = cy.id



select * from HLA_codes;
select * from HLA_hierarchy where parentid = -1


select c.id , count(*)
 from HLA_codes c , HLA_hierarchy h where c.id = h.id and c.definingid = 1
 group by c.id


select h.parentid , count(*)
  from HLA_codes c , HLA_hierarchy h
 where c.id = h.id and c.definingid = 1
 group by h.parentid


select gh.parentid , count(*)
  from HLA_codes c , HLA_hierarchy h , HLA_hierarchy gh
 where gh.id = h.parentid and h.id = c.id
   and c.definingid = 1
 group by gh.parentid



select 'codes: ' , count(*) from codes
union all
select 'code_attributes: ' , count(*) from code_attributes
union all
select 'code_hierarchy: ' , count(*) from code_hierarchy;

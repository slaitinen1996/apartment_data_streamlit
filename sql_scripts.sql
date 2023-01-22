--delete from stg_asunnot where id=16852100

UPDATE asunnot
SET (status, myyntikesto) =('myyty', datetime('now')-pvm)
WHERE asunnot.id IN (select a.id as id from asunnot a
left join stg_asunnot sa on a.id=sa.id
where sa.id IS NULL) --Myydyt, näissä updettaa status

INSERT INTO asunnot
WITH RECURSIVE uudet as (select sa.* from stg_asunnot sa 
left join asunnot a on sa.id=a.id
where a.id IS NULL)
SELECT * FROM uudet; -- Uudet asunnot lisätään


select oa.Kaupunginosa, oa.Huoneita, count(Neliohinta) , avg(oa.Neliohinta) as neliohinta_avg, avg(oa.Hoitovastike_m2) as Hoitovastike_m2_avg,
avg(oa.Asuinpinta_ala) as Asuinpinta_ala 
from oikotie_asunnot oa
group by oa.Kaupunginosa, oa.Huoneita; -- Aggregates
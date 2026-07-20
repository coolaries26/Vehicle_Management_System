-- Scenario for getting all complaints records from api 

-- DELETE FROM maintenance.job_card_part;
delete from maintenance.job_card_part where job_card_id IN(
	select job_card_id 
	from transact.maintenance_job_card 
	where inspection_id is NULL
);

-- DELETE FROM transact.maintenance_job_card;
delete from transact.maintenance_job_card
where inspection_id in (select inspection_id
FROM maintenance.technician_inspection
WHERE complaint_id IN (
    SELECT complaint_id
    FROM maintenance.vehicle_complaint
    WHERE vehicle_id IS NULL
       OR driver_id IS NULL
));

-- DELETE FROM maintenance.technician_inspection;
DELETE
FROM maintenance.technician_inspection
WHERE complaint_id IN (
    SELECT complaint_id
    FROM maintenance.vehicle_complaint
    WHERE vehicle_id IS NULL
       OR driver_id IS NULL
);

--DELETE FROM maintenance.vehicle_complaint;
DELETE
FROM maintenance.vehicle_complaint
WHERE vehicle_id IS NULL
   OR driver_id IS NULL;

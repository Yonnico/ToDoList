BEGIN;
UPDATE tasks SET done = True WHERE user_id = 1 AND task_index = 1;
COMMIT;

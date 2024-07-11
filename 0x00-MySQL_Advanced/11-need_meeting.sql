-- This is an SQL script to create an view need_meeting.
CREATE VIEW need_meeting AS SELECT name from students WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < DATE(CURDATE() - INTERVAL 1 MONTH));

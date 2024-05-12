-- 7-average_score.sql
-- Task 7: ComputeAverageScoreForUser stored procedure

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE avg_score FLOAT;

    -- Calculate total score for the user
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;

    -- Calculate total number of projects for the user
    SELECT COUNT(DISTINCT project_id) INTO total_projects FROM corrections WHERE user_id = user_id;

    -- Calculate average score
    IF total_projects > 0 THEN
        SET avg_score = total_score / total_projects;
    ELSE
        SET avg_score = 0;
    END IF;

    -- Update the average_score for the user
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END;
//
DELIMITER ;


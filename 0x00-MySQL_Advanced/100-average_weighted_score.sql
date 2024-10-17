-- Script that coumputes Average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_weighted_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate total weighted score
    SELECT SUM(corrections.score * projects.weight)
        INTO total_weighted_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Calculate total weight
    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Update the average score for the user
    IF total_weight = 0 THEN
        UPDATE users
            SET average_score = 0
            WHERE id = user_id;
    ELSE
        UPDATE users
            SET average_score = total_weighted_score / total_weight
            WHERE id = user_id;
    END IF;
END $$
DELIMITER ;

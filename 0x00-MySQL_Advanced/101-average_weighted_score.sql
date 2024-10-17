-- Script that coumputes Average weighted score for all students
utes Average weighted score for all students
utes Average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_weighted_score INT;
    DECLARE total_weight INT;

    -- Declare a cursor to iterate over all users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Declare a continue handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through each user
    read_loop: LOOP
        FETCH user_cursor INTO user_id;

        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Initialize the totals
        SET total_weighted_score = 0;
        SET total_weight = 0;

        -- Calculate the total weighted score for the current user
        SELECT COALESCE(SUM(corrections.score * projects.weight), 0)
            INTO total_weighted_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the total weight for the current user
        SELECT COALESCE(SUM(projects.weight), 0)
            INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Update the average score for the current user
        UPDATE users
            SET average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight)
            WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END $$
DELIMITER ;

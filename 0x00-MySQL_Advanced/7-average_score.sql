-- This stored procedure computes and stores the average score for a student.
-- Drops the stored procedure if it already exists to avoid conflicts when creating a new one
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Changing the delimiter to $$ to allow for defining the procedure
DELIMITER $$

-- Create the stored procedure ComputeAverageScoreForUser
CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT -- Input parameter: ID of the user for whom we are calculating the average score
)
BEGIN
    -- Declare variables to store the total score and the number of projects for the user
    DECLARE total_score INT DEFAULT 0;  -- Initialize total_score to 0
    DECLARE projects_count INT DEFAULT 0;  -- Initialize projects_count to 0

    -- Calculate the total score for the user from the corrections table
    SELECT SUM(score)
    INTO total_score  -- Store the sum of the scores in total_score
    FROM corrections
    WHERE corrections.user_id = user_id;  -- Select records where the user_id matches the input

    -- Count the number of projects the user has corrections for
    SELECT COUNT(*)
    INTO projects_count  -- Store the count of projects in projects_count
    FROM corrections
    WHERE corrections.user_id = user_id;  -- Select records where the user_id matches the input

    -- Update the user's average score in the users table
    UPDATE users
    SET users.average_score = IF(projects_count = 0, 0, total_score / projects_count)
        -- If the user has no projects (projects_count = 0), set average_score to 0,
        -- otherwise calculate the average by dividing total_score by projects_count
    WHERE users.id = user_id;  -- Ensure that only the record for the specified user is updated
END $$

-- Resetting the delimiter back to the default
DELIMITER ;

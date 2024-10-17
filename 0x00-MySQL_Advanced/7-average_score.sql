-- This stored procedure computes and stores the average score for a student.

DELIMITER $$  -- Change the delimiter to allow for procedure definition

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT  -- User ID linked to an existing user
)
BEGIN
    DECLARE average_score DECIMAL(10, 2);  -- Variable to hold the computed average score

    -- Compute the average score for the user
    SELECT AVG(score) INTO average_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average score in the users table (assuming an average_score column exists)
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END $$

DELIMITER ;  -- Reset the delimiter back to the default

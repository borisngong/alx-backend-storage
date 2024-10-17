-- This stored procedure adds a new correction for a student
-- and creates a new project if it doesn't already exist.

DELIMITER $$

CREATE PROCEDURE AddBonus (
    IN user_id INT,           -- User ID linked to an existing user
    IN project_name VARCHAR(255),  -- Project name (new or existing)
    IN score INT              -- Score value for the correction
)
BEGIN
    DECLARE project_id INT;   -- Variable to hold the project ID

    -- Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- If project_id is NULL, it means the project does not exist
    IF project_id IS NULL THEN
        -- Create the new project
        INSERT INTO projects (name) VALUES (project_name);
        -- Get the ID of the newly created project
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Now, insert the score into the corrections table
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END $$

DELIMITER ;

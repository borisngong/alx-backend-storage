-- Script to create the function SafeDiv
-- if it already exists to avoid conflicts when creating a new one
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (
    a INT,
    b INT
)
RETURNS FLOAT  -- The function will return a FLOAT value
DETERMINISTIC  -- function will always return the same result for same input
BEGIN
    DECLARE result FLOAT DEFAULT 0;  -- Initialize 'result' to 0

    -- prevent division by zero
    IF b != 0 THEN
        SET result = a / b;
    END IF;

    RETURN result;
END $$

-- Reset the delimiter back to the default
DELIMITER ;

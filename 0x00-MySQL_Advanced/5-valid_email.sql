-- This trigger resets the valid_email attribute to false (0)
-- when the email of a user is changed in the users table.

DROP TRIGGER IF EXISTS reset_valid_email;  -- Drop the trigger if it already exists

DELIMITER $$  -- Change the delimiter to allow for trigger definition

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users  -- Trigger activates before an update on the users table
FOR EACH ROW  -- Execute for each row being updated
BEGIN
    -- Check if the email is being changed
    IF OLD.email != NEW.email THEN
        -- Reset valid_email to false (0) if the email has changed
        SET NEW.valid_email = 0;  -- Reset valid_email to false
    END IF;
END $$

DELIMITER ;  -- Reset the delimiter back to the default

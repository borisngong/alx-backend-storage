-- This trigger reduces the quantity of an item in the items table
-- after a new order is inserted into the orders table.
-- It uses the item name to identify which item's quantity to decrease.

DROP TRIGGER IF EXISTS reduce_quantity;  -- Drop the trigger if it already exists

DELIMITER $$  -- Change the delimiter to allow for trigger definition

CREATE TRIGGER reduce_quantity
AFTER INSERT ON orders  -- Trigger activates after an insert on the orders table
FOR EACH ROW  -- Execute for each row that is inserted
BEGIN
    -- Update the items table to reduce the quantity of the item ordered
    UPDATE items
    SET quantity = quantity - NEW.number  -- Subtract the quantity ordered
    WHERE name = NEW.item_name;  -- Identify the item by its name
END $$

DELIMITER ;  -- Reset the delimiter back to the default

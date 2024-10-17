-- This script creates an index on the first letter of the name column and the score column in the names table.

-- Step 1: Drop the index if it already exists (to avoid conflicts)
DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Step 2: Create the index on the first letter of the name column and the score column
CREATE INDEX idx_name_first_score ON names (SUBSTRING(name, 1, 1), score);

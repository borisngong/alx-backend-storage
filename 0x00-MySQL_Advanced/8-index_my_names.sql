-- This script creates an index on the first letter of the name column in the names table.

-- Drop the index if it already exists (to avoid conflicts)
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create the index on the first letter of the name column
CREATE INDEX idx_name_first ON names(name(1));

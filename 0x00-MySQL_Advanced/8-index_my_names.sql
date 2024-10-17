-- Script that creates an idx on the 1st letter of name column

-- Drop the index if it already exists (to avoid conflicts)
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create the index on the first letter of the name column
CREATE INDEX idx_name_first ON names(name(1));

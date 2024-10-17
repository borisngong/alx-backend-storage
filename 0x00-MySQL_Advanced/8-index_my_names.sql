-- Script that creates an idx on the 1st letter of name column
CREATE INDEX idx_name_first ON names(name(1));

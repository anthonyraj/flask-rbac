-- RBAC Schema Creation 

-- Creating Lab Schema
set schema 'emctest';
\i reset_sequence.sql

set schema 'universal';
\i reset_sequence.sql

set schema 'safetytest';
\i reset_sequence.sql

-- Creating OEM Schema
set schema 'collaboration';
\i reset_sequence.sql

set schema 'equipa';
\i reset_sequence.sql

set schema 'manufacto';
\i reset_sequence.sql

set schema 'acme';
\i reset_sequence.sql
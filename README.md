# crmSiteBackend
167.172.107.185

Azamat1123HIk@mail

998991234567
azamat1123


git stash push --include-untracked



sudo -u postgres psql

CREATE DATABASE hikvisionsts;
CREATE USER azamatdev WITH PASSWORD 'azamat1796hik';

ALTER ROLE azamatdev SET client_encoding TO 'utf8';

ALTER ROLE azamatdev SET default_transaction_isolation TO 'read committed';

ALTER ROLE azamatdev SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE hikvisionsts TO azamatdev;

ALTER DATABASE hikvisionsts OWNER TO azamatdev;
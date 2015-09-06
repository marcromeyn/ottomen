FROM postgres:9.4
RUN psql <<- EOSQL
    CREATE USER docker;
    CREATE DATABASE ottomen;
    CREATE DATABASE ottomen_test;
    GRANT ALL PRIVILEGES ON DATABASE ottomen TO docker;
    GRANT ALL PRIVILEGES ON DATABASE ottomen_test TO docker;
EOSQL
#! /usr/bin/env bash

# Let the DB start
python ./app/db/db_check.py

alembic upgrade head

# Create initial test data in DB
python ./tests/init_db.py
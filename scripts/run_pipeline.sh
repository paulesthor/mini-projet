#!/bin/bash
# run_pipeline.sh

echo "--- Starting Pipeline ---"

# 1. Wait for DB
./scripts/wait-for-db.sh
if [ $? -ne 0 ]; then
    echo "Error: Database check failed."
    exit 1
fi

# 2. Initialize DB (tables)
# Note: In our Docker setup, init-db.sql is usually run by the container on first startup.
# However, if we need to ensure tables exist or reset them, we could run:
# mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /app/scripts/init-db.sql
# But typically init-db.sql uses IF NOT EXISTS, so running it again is safe.
echo "Initializing/Checking Database Schema..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" --ssl=0 < /app/scripts/init-db.sql
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed."
    exit 1
fi

# 3. Run ETL Pipeline & Report
echo "Running Python Pipeline..."
python /app/src/main.py
if [ $? -ne 0 ]; then
    echo "Error: Python pipeline failed."
    exit 1
fi

echo "--- Pipeline Completed Successfully ---"
exit 0

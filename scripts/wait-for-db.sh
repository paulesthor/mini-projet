#!/bin/bash
# wait-for-db.sh

MAX_RETRIES=30
RETRY_INTERVAL=2

echo "Waiting for database connection..."

for i in $(seq 1 $MAX_RETRIES); do
    if mysqladmin ping -h "$DB_HOST" -u "$DB_USER" --password="$DB_PASSWORD" --ssl=0 --silent; then
        echo "Database is ready!"
        exit 0
    fi
    echo "Attempt $i/$MAX_RETRIES: Database not ready yet, waiting ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

echo "Error: Database did not become ready in time."
exit 1

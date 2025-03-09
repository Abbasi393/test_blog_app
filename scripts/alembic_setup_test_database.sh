#!/bin/bash

DB_NAME="blog_db"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"


read -s -p "Enter password for user '$DB_USER': " DB_PASS
echo


echo "Creating test database...."
PGPASSWORD="$DB_PASS" psql -U postgres -h "$DB_HOST" -c "DROP DATABASE IF EXISTS $DB_NAME;"
PGPASSWORD="$DB_PASS" psql -U postgres -h "$DB_HOST" -c "CREATE DATABASE $DB_NAME;"


export DATABASE_URL="postgresql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME"
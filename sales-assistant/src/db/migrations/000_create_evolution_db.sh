#!/bin/bash
# Create a dedicated database for Evolution API Prisma migrations.
# || true prevents a failure if the database already exists.
createdb --username="$POSTGRES_USER" --owner="$POSTGRES_USER" evolution 2>/dev/null || true

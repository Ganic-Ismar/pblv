# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Set the environment variables for the PostgreSQL database
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB mydatabase

# Copy the SQL file to the container
COPY smartcharge.sql /docker-entrypoint-initdb.d/
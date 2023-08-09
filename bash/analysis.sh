#!/bin/bash

# Database credentials
USER="root"
PASSWORD="root"
DATABASE="db"
HOST="localhost"

# SQL query
QUERY="SELECT traffic_data.* FROM traffic_data JOIN employee ON traffic_data.id_num = employee.NUM WHERE employee.MAC != traffic_data.src_mac;"

# Execute SQL query and export to CSV
mysql -h $HOST -u $USER -p$PASSWORD $DATABASE -e "$QUERY" > output.csv

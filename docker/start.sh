#!/bin/sh

# Test services we need before starting our service.
echo "Start script: waiting for needed services"
python3 /kafka_wait_for_topics.py
python3 /mysql_check.py

./wait_for.sh "$MONASCA_URI"
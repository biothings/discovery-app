#!/bin/bash

indices=("discover_schema" "discover_dataset" "discover_schema_class")
for index in "${indices[@]}"; do
  curl -X POST "http://localhost:9200/$index/_search?scroll=1m&size=100" \
  -H "Content-Type: application/json" \
  -d '{"query": {"match_all": {}}}' > "${index}.json"
done

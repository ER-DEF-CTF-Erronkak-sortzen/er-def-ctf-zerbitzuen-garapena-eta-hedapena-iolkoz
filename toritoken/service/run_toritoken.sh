#!/usr/bin/env bash

docker-compose -f "$SERVICES_PATH/toritoken/docker-compose.yml" up -d --build
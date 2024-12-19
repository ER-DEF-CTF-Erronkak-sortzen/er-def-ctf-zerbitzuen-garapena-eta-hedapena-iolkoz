#!/usr/bin/env bash

docker stop toritoken_api_1 
docker stop toritoken_web_1
docker stop toritoken_db_1
ddocker rm toritoken_api_1 
docker rm toritoken_web_1
docker rm toritoken_db_1
#!/usr/bin/bash
curl -s -S "https://hub.docker.com/v2/repositories/library/$@/tags/" | jq '."results"[]["name"]' |sort

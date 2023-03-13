#!/bin/bash
docker build -t cloud ./Cloud
docker build -t edge ./Edge
docker compose up

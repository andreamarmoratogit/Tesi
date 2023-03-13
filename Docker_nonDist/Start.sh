#!/bin/bash
docker build -t cloud_ND ./Cloud
docker build -t edge_ND ./Edge
docker compose up

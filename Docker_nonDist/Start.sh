#!/bin/bash
docker build -t cloud_nd ./Cloud
docker build -t edge_nd ./Edge
docker compose up

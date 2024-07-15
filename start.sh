#!/bin/bash

./backend.sh &

sleep 5

./frontend.sh &

wait
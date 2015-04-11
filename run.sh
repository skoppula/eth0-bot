#!/bin/bash

while true; do
	current_time=$(date "+%H.%M.%S")
	python bot.py > logs/$current_time.txt
	sleep 5
done

#!/bin/bash

while true; do
	current_time=$(date "+%H.%M.%S")
	python bot.py 2>&1 | tee logs/$current_time.txt
	sleep 5
done

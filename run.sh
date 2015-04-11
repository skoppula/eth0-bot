#!/bin/bash

while true; do
	T="$(date +%s)"
	python bot.py > {$T}.txt
	sleep 5
done

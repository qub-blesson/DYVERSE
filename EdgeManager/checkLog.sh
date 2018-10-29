#!bin/bash

APP_PATH=$1
ACTION=$2
LOG="log.tmp"

# extract requests: lines not starting with "Bottle", "start", "end"
grep ^[^Bottle\^Listen\^Hit\^start\^end] $APP_PATH/serverLog > $APP_PATH/$LOG

case $ACTION in 
"request")
    # count lines of requests
    REQUEST=($(wc -l $APP_PATH/$LOG))
	echo $REQUEST
	;;
"data")
	# sum amount of data transferred (the last field of log)
	awk -F" " '{print $NF}' < $APP_PATH/$LOG > $APP_PATH/tmp
	if [ -s $APP_PATH/tmp ]
 	then 
#		echo "tmp is not empty"
		DATA=$(paste -sd+ $APP_PATH/tmp | bc)
	else
#		echo "tmp is empty"
		DATA=0
	fi
	echo $DATA
	;;
"reset")
	# clean log for next round recording
	truncate -s 0 $APP_PATH/serverLog
	rm $APP_PATH/tmp $APP_PATH/$LOG
	;;
"user")
	# remove unpritable ASCII character (^@), added to first request after truncate
    # sum no. of users (the first field of log)
	USER=$(tr -dc '[\011\012\015\040-\176]' < $APP_PATH/$LOG | cut -d " " -f1 | uniq | wc -l)
	echo $USER
esac

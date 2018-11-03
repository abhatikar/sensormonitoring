#!/bin/bash
if [ $1 == '-h' ];
then
	echo "usage cleanall.sh all Will clean up the images as well as containers (Use with caution)"
	echo "usage cleanall.sh Will clean up the running containers only"
fi

for image in backend subscriber
do
	id=$(docker ps | grep $image | awk '{ print $1 }')
	docker kill $id
	if [ $1 == 'all' ];
       	then
		docker image rm $image -f
	fi
done

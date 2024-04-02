#!/bin/bash
version="1"
image_name="demo_squelettisation"
echo "The image is building... (this may take a while)"
docker build -t $image_name:v$version .
echo "Would you like the image to be saved in a .tar.gz file ? [y/n]"
read choice
case $choice in
y)
	file_name="image_"$image_name"_v"$version".tar.gz"
	echo "The image is being saved to '$file_name'... (this may take a while)"
	docker image save $image_name:v$version | gzip > $file_name 
	;;
*)
	exit
	;;
esac

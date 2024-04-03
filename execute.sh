#!/bin/bash
execute_docker () {
	xhost_state=$(xhost)
	if [[ ${xhost_state:15:8} != 'disabled' ]]; then
		echo $'X11 access control is enabled. To use this program, it needs to be disabled.\nWould you like it to be disabled ? [y/n]\n(the command "xhost -" can be used to enable it back after using the program)'
		read choice
		case $choice in
		y)
			xhost +
			;;
		*)
			exit
			;;
		esac
	fi
	echo $'What would you like to do?\n1. Execute with webcam\n2. Execute with phone app "IP Webcam"\n3. Execute with nano2 5G box\n4. Execute with another RTSP source'
	read choice
	case $choice in
	1)
		echo 'The container is starting...'
		docker run -i --rm --network host --gpus all --device=/dev/video0:/dev/video0 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $image_name:$installed_version python3 Demo_squelet/ia_squelet.py
		;;
	2)
		echo 'The container is starting... (please wait for it to prompt for IP)'
		docker run -i --rm --network host --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $image_name:$installed_version python3 Demo_squelet/ia_squelet.py --source prompt_ip_webcam
		;;
	3)
		echo 'The container is starting...'
		docker run -i --rm --network host --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $image_name:$installed_version python3 Demo_squelet/ia_squelet.py --source nano2
		;;
	4)
		echo 'The container is starting... (please wait for it to prompt for link)'
		docker run -i --rm --network host --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $image_name:$installed_version python3 Demo_squelet/ia_squelet.py --source prompt_rtsp
		;;
	*)
		echo 'Wrong choice'
		;;
	esac
}
image_name="demo_squelettisation"
image_file_format="^image_demo_squelettisation_(v[0-9]+(\.[0-9]+)*)\.tar.gz$"
image_file=$(ls | grep -oP "$image_file_format" | sort -V | tail -n 1)
installed_version=$(docker images $image_name --format "{{.Tag}}" | sort -V | tail -n 1)
if [ "$image_file" != "" ] && [[ $image_file =~ $image_file_format ]]; then
	image_file_version=${BASH_REMATCH[1]}
	echo "The latest image file found was $image_file"
	if [[ $installed_version == "" ]]; then
		echo "No version installed, installation will proceed (this may take a few minutes)"
		docker load < $image_file
		installed_version=$image_file_version
		execute_docker
	else
		echo "An installed version was found: $installed_version"
		if [[ $image_file_version != $installed_version ]]; then
			echo "This version is different than the latest image available, replacement will proceed (this may take a few minutes)"
			docker rmi $image_name:$installed_version
			docker load < $image_file
			installed_version=$image_file_version
			execute_docker
		else
			echo "The version from the file is identical to the one installed"
			execute_docker
		fi
fi
else
	echo "No image file was found"
	if [[ $installed_version == "" ]]; then
		echo "No version is installed, and no image file was found, cannot execute"
	else
		echo "The currently installed version ($installed_version) will execute"
		execute_docker
	fi
fi

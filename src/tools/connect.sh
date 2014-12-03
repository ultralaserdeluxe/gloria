#!/bin/bash
# Script will try to connect to beagleboard over bluetooth
# If successful, or already connected it will try to open a ssh-session
# Usage:
# sudo connect.sh
# First time invoked will ask for ip to be used. This ip will be saved in connect.conf
# Saved ip is changed either by changing content of connect.conf or by deleting connect.conf and invoking connect.sh anew
# Alternative usage:
# sudo connect.sh <ip-address>
# Will try to connect with specified ip address. Does not affect saved ip in connect.conf
main() {
	local conf_file="./connect.conf"		# Specify conf_file
	local bt_interface="bnep0"				# Specify BT interface
	local ssh_server="ubuntu@192.168.99.1"	# Specify ssh server

	if [ "$#" -ne 1 ]
	then
		# No argument - Use conf_file
		if [ ! -e $conf_file ]
			then
			# create conf if doesnt exist
			echo "Choose an unused ip:"
			read local ip
			echo $ip > $conf_file
		else
			# else read from file
			local ip=$(head -n 1 $conf_file)
		fi
	else
		# Use argument
		local ip=$1
	fi
	echo Using ip $ip

	# Check if connected
	local bluetooth="$(ifconfig | egrep $bt_interface)"
	if [ -z "${bluetooth}" ]
	then
		# If bluetooth not connected, connect
		echo Connecting...
		sh ./connect_bt.sh $ip
	else
		echo Already connected!
	fi

	# Check if connected successfully
	local bluetooth="$(ifconfig | egrep $bt_interface)"
	if [ -z "${bluetooth}" ]
	then
		echo Failed to connect.
	else
		# Connect to ssh
		echo Setting up ssh.
		ssh $ssh_server
		# TODO: Send password aswell
	fi
}

main $1
exit 1

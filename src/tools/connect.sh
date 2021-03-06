#!/bin/bash
# Script will try to connect to beagleboard over bluetooth
# If successful, or already connected it will try to open a ssh-session
# ----------------------
# Expect:
# Expect is a program that can be found in ubuntu/debians standardrepo.
# If expect is installed, we wont have to enter password upon logging in
# ----------------------
# Usage:
# sudo connect.sh
# First time invoked will ask for ip to be used. This ip will be saved in connect.conf
# Saved ip is changed either by changing content of connect.conf or by deleting connect.conf and invoking connect.sh anew
# ----------------------
# Using temporary ip:
# sudo connect.sh <ip-address>
# Will try to connect with specified ip address. Does not affect saved ip in config
# ----------------------
# Resetting config
# sudo connect.sh reset
# ----------------------
main() {
	local conf_file="./connect.conf"		# Specify conf_file
	local bt_interface="bnep0"				# Specify BT interface
	local ssh_server="ubuntu@192.168.99.1"	# Specify ssh server
	local ssh_password="temppwd"			# Specify ssh password - Possible security issue

	local ip
	if [ "$#" -ne 1 ]; then
		# No argument - Use conf_file
		if [ ! -e $conf_file ]; then
			# create conf if doesnt exist
			echo "Choose an unused ip-address:"
			read ip
			echo $ip > $conf_file
		else
			# else read from file
			ip=$(head -n 1 $conf_file)
		fi
	elif [ $1 == "reset" ]; then
		echo "Resetting..."
		rm $conf_file
		exit 1
	else
		# Use argument as ip
		ip=$1
	fi
	echo "Using ip $ip"

	# Check if connected, connect if not
	local bluetooth="$(ifconfig | egrep $bt_interface)"
	if [ -z "${bluetooth}" ]
	then
		# If bluetooth not connected, try to connect
		echo "Connecting..."
		sh ./connect_bt.sh $ip
	else
		echo "Already connected!"
	fi

	# Check if connected successfully"
	local bluetooth="$(ifconfig | egrep $bt_interface)"
	if [ -z "${bluetooth}" ]; then
		echo "Failed to connect."
	else
		# If expect is installed, connect and provide password
		local expect=$(which expect)
		if [[ ${#expect} > 0 ]]; then
			# Connect using separate expect script, entering password.
			./connect_ssh.sh $ssh_server $ssh_password
		else
			# Connect to ssh

			echo "Connecting over SSH."
			echo "Consider installing Expect (apt-get install expect) to make the process even easier."
			ssh $ssh_server
		fi
	fi
}

main $1
exit 1

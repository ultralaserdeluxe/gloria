#!/usr/bin/expect -f
# Script will try to connect to a ssh-server
# If
# ----------------------
# Usage:
# connect_ssh.sh <ssh_server> <ssh_password

set timeout 60

spawn ssh [lindex $argv 0]

expect {
	"yes/no" { send "yes" }
	"assword: " { send "[lindex $argv 1]\r" }
}
expect {
	"assword: " { send "[lindex $argv 1]\r" }
	"?*" {}
}

interact

exit

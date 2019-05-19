import socket
import json

def send_to_env_mac():
	with open("mac_wakeup_addr.json") as f:
		mac_address = json.load(f)["mac_address"]
	send_package(mac_address)

def send_package(mac):
	# Split mac parts
	mac_address_array = mac.split(":")

	# Mac address of machine that needs to be woken up
	mac_array = []
	for i in mac_address_array:
		phase1 = int('0x' + i, 16)
		mac_array.append(phase1)

	# Set up socket
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server.bind(("", 44444))
	# Create wake on lan package (must be length of 110)
	arr = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
	for i in range(0, 16):
		arr += mac_array
	message = bytes(arr)
	# Send package
	print("WOF message: " + str(message))
	server.sendto(message, ('<broadcast>', 9))

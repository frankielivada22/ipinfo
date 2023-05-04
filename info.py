import time 
import sys
import os

"""
***************************************************
             IP Info Documentation               
***************************************************

This script allows you to input an IPv4 address and retrieve various information related to that address.

The following functions are defined in the script:

- is_valid_ipv4(ip_address)
  Takes an IP address as input and returns a boolean value indicating whether the IP address is valid or not.

- ip_to_binary(ip_address)
  Takes an IP address as input and returns its binary representation.

- get_subnet_mask_and_class(ip)
  Takes an IP address as input and returns the subnet mask and class of the IP address.

- ip_to_int(ip)
  Takes an IP address as input and returns its integer representation.

- int_to_ip(ip_int)
  Takes an integer representation of an IP address as input and returns the IP address as a string.

- get_ip_range(ip_address, subnet_mask)
  Takes an IP address and subnet mask as input and returns the range of IP addresses that fall within the subnet.

- get_broadcast_address(ip_address, subnet_mask)
  Takes an IP address and subnet mask as input and returns the broadcast address.

- get_network_address(ip_address, subnet_mask)
  Takes an IP address and subnet mask as input and returns the network address.

- get_total_ips(subnet_mask)
  Takes a subnet mask as input and returns the total number of IP addresses in the subnet.

- get_usable_ips(subnet_mask)
  Takes a subnet mask as input and returns the number of usable IP addresses in the subnet.

- is_private(ip_address)
  Takes an IP address as input and returns a boolean value indicating whether the IP address is a private address or not.

- cidr_notation(ip_address, subnet_mask)
  Takes an IP address and subnet mask as input and returns the CIDR notation for the subnet.

- get_wildcard_mask(subnet_mask)
  Takes a subnet mask as input and returns the wildcard mask.

- ipv4_to_ipv6(ipv4_address)
  Takes an IPv4 address as input and returns its IPv6 representation.

- ip_to_decimal(ip_address)
  Takes an IP address as input and returns its decimal representation.

- neighboring_networks(network_address, subnet_mask)
  Takes a network address and subnet mask as input and returns the previous and next network addresses.

- longest_consecutive_bits(subnet_mask)
  Takes a subnet mask as input and returns the number of consecutive ones and zeros in the binary representation of the subnet mask.

To use the script, input an IPv4 address as a command line argument or when prompted.

The script will then output various information related to the IP address, including its binary representation, subnet mask, IP address range, broadcast address, network address, and more. The information will be stylized in a box using the create_box_with_text() function.

Enjoy!
"""




try:
	ip = sys.argv[1]
except:
	ip = input("Please enter an IP: ")




def is_valid_ipv4(ip_address):
	octets = ip_address.split('.')

	if len(octets) != 4:
		return False

	for octet in octets:
		if not octet.isdigit() or not (0 <= int(octet) <= 255):
			return False

	return True

try:
	ss = is_valid_ipv4(ip)
	if ss == False:
		print("Please enter a valid IPv4 address")
		sys.exit(0)
except:
	print("Was unable to verify the IP address")
	sys.exit(0)


def ip_to_binary(ip_address):
	octets = ip_address.split('.')

	binary_ip = ''

	for octet in octets:
		octet = int(octet)
		octet_binary = ''

		powers_of_two = [128, 64, 32, 16, 8, 4, 2, 1]

		for power in powers_of_two:
			if octet >= power:
				octet_binary += '1'
				octet -= power
			else:
				octet_binary += '0'

		octet_binary += '.'
	
		binary_ip += octet_binary

	return binary_ip[:-1]

def get_subnet_mask_and_class(ip):
	octets = ip.split('.')
	first_octet = int(octets[0])

	ip_class = None
	subnet_mask = None

	if 1 <= first_octet <= 126:
		ip_class = 'A'
		subnet_mask = '255.0.0.0'
	elif 128 <= first_octet <= 191:
		ip_class = 'B'
		subnet_mask = '255.255.0.0'
	elif 192 <= first_octet <= 223:
		ip_class = 'C'
		subnet_mask = '255.255.255.0'
	else:
		raise ValueError("The IP address is not a Class A, B, or C address.")

	return subnet_mask, ip_class

def ip_to_int(ip):
	octets = [int(octet) for octet in ip.split('.')]
	return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]

def int_to_ip(ip_int):
	return '.'.join([str(ip_int >> (8 * i) & 0xFF) for i in range(4)[::-1]])

def get_ip_range(ip_address, subnet_mask):
	ip_int = ip_to_int(ip_address)
	subnet_int = ip_to_int(subnet_mask)
	network_int = ip_int & subnet_int

	network_address = int_to_ip(network_int)
	broadcast_address_int = network_int | (~subnet_int & 0xFFFFFFFF)
	broadcast_address = int_to_ip(broadcast_address_int)

	first_ip_int = network_int + 1
	last_ip_int = broadcast_address_int - 1

	first_ip = int_to_ip(first_ip_int)
	last_ip = int_to_ip(last_ip_int)

	return f'{first_ip} - {last_ip}'

def get_broadcast_address(ip_address, subnet_mask):
	ip_int = ip_to_int(ip_address)
	subnet_int = ip_to_int(subnet_mask)
	network_int = ip_int & subnet_int

	broadcast_address_int = network_int | (~subnet_int & 0xFFFFFFFF)
	broadcast_address = int_to_ip(broadcast_address_int)

	return broadcast_address

def get_network_address(ip_address, subnet_mask):
	ip_int = ip_to_int(ip_address)
	subnet_int = ip_to_int(subnet_mask)
	network_int = ip_int & subnet_int

	network_address = int_to_ip(network_int)

	return network_address

def get_total_ips(subnet_mask):
	subnet_int = ip_to_int(subnet_mask)
	total_ips = 2 ** (32 - bin(subnet_int).count('1'))
	return total_ips

def get_usable_ips(subnet_mask):
	subnet_int = ip_to_int(subnet_mask)
	total_ips = 2 ** (32 - bin(subnet_int).count('1'))
	usable_ips = total_ips - 2  # Subtract network and broadcast addresses
	return usable_ips

def is_private(ip_address):
	octets = [int(octet) for octet in ip_address.split('.')]
	
	if octets[0] == 10 or (octets[0] == 172 and 16 <= octets[1] <= 31) or (octets[0] == 192 and octets[1] == 168):
		return True
	return False

def cidr_notation(ip_address, subnet_mask):
	subnet_int = ip_to_int(subnet_mask)
	prefix_length = bin(subnet_int).count('1')
	return f'{ip_address}/{prefix_length}'

def get_wildcard_mask(subnet_mask):
	subnet_int = ip_to_int(subnet_mask)
	wildcard_int = ~subnet_int & 0xFFFFFFFF
	return int_to_ip(wildcard_int)

def ipv4_to_ipv6(ipv4_address):
	octets = [int(octet) for octet in ipv4_address.split('.')]
	ipv6_address = f'::ffff:{octets[0]:02x}{octets[1]:02x}:{octets[2]:02x}{octets[3]:02x}'
	return ipv6_address

def ip_to_decimal(ip_address):
	octets = [int(octet) for octet in ip_address.split('.')]
	return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]

def neighboring_networks(network_address, subnet_mask):
	network_int = ip_to_int(network_address)
	subnet_int = ip_to_int(subnet_mask)
	host_bits = ~subnet_int & 0xFFFFFFFF

	prev_network_int = network_int - (host_bits + 1)
	next_network_int = network_int + (host_bits + 1)

	return int_to_ip(prev_network_int), int_to_ip(next_network_int)

def longest_consecutive_bits(subnet_mask):
	subnet_int = ip_to_int(subnet_mask)
	subnet_binary = format(subnet_int, '032b')

	max_consecutive_ones = 0
	max_consecutive_zeros = 0

	count_ones = 0
	count_zeros = 0

	for bit in subnet_binary:
		if bit == '1':
			count_ones += 1
			max_consecutive_zeros = max(max_consecutive_zeros, count_zeros)
			count_zeros = 0
		else:
			count_zeros += 1
			max_consecutive_ones = max(max_consecutive_ones, count_ones)
			count_ones = 0

	max_consecutive_zeros = max(max_consecutive_zeros, count_zeros)
	max_consecutive_ones = max(max_consecutive_ones, count_ones)

	return max_consecutive_ones, max_consecutive_zeros













def create_box_with_text(text):
	text = text.replace('\t', '    ')
	
	lines = text.split('\n')

	max_line_length = max(len(line) for line in lines)
	box_width = max_line_length + 4
	box_height = len(lines) + 2

	top_border = '+' + '-' * (box_width - 2) + '+'
	bottom_border = top_border

	box_content = [top_border]

	for line in lines:
		padding_left = (max_line_length - len(line)) // 2
		padding_right = max_line_length - len(line) - padding_left
		box_line = f'| {" " * padding_left}{line}{" " * padding_right} |'
		box_content.append(box_line)

	box_content.append(bottom_border)

	return '\n'.join(box_content)




binary_ip = ip_to_binary(ip)
subnet_mask,ip_class = get_subnet_mask_and_class(ip)
subnet_mask_binary = ip_to_binary(subnet_mask)
ip_range = get_ip_range(ip, subnet_mask)
broadcast_ip = get_broadcast_address(ip, subnet_mask)
broadcast_ip_binary = ip_to_binary(broadcast_ip)
network_address = get_network_address(ip, subnet_mask)
total_ips = get_total_ips(subnet_mask)
usable_ips = get_usable_ips(subnet_mask)
ip_type = is_private(ip)
notation = cidr_notation(ip, subnet_mask)
wildcard = get_wildcard_mask(subnet_mask)
ipv6 = ipv4_to_ipv6(ip)
decimal = ip_to_decimal(ip)
prev_network, next_network = neighboring_networks(network_address, subnet_mask)
longest_bits = longest_consecutive_bits(subnet_mask)



string = (f"""
[IP INFO]

IP: {ip}
Binary: {binary_ip}

[Subnet info]
Class: {ip_class}
Subnet mask: {subnet_mask}
Subnet mask binary: {subnet_mask_binary}
Longest bits: {longest_bits}

[Broadcast info]
Address: {broadcast_ip}
Binary: {broadcast_ip_binary}

[CIDR info]
Range: {ip_range}
Notation: {notation}
Wildcard: {wildcard}

[Network]
Type: {"private" if ip_type else "public"}
Address: {network_address}
Total IPs: {total_ips}
Usable IPs: {usable_ips}
Prev Network: {prev_network}
Next Network: {next_network}

[Other]
IPv6: {ipv6}
Decimal: {decimal}

	""")

print(create_box_with_text(string))
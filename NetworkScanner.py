#!/usr/bin/env python

#import scapy (it is a class for networking scripts)
import scapy.all as scapy
#import optparse (it is used to collect options from user such as in command line when user adds -t)
import optparse

#This function is used to colect options from user, create --help for info and uses if function
def get_arguments():

#Create a variable to store the option the user chooses
    parser = optparse.OptionParser()
#Create the option to be added by user and the help menu + dest is where the option will be stored
    parser.add_option("-t", "--target", dest="target", help="Target IP")
    (options, arguments) = parser.parse_args()
#Usual if function
    if not options.target:
        parser.error("[-] PLease choose an IP address, use --help for more info")
    return options

#This function will scan for target
def scan(ip):

#Send an arp request and store it in a variable called arp_request
    arp_request = scapy.ARP(pdst=ip)
#Send a broadcast using a mac address and store it in a variable called broadcast
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#Combine both requets
    arp_request_broadcast = broadcast/arp_request
#The send and received packets using scacpy.arp will create two LISTS
#First list got answered requests, the second is the unanswered requests
#Verbose, is to not print unncessary things by scapy, timeout to wait for 1 sec after each request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

#Create a variable with empty list because we will create a dictoniary list (uses key instead of value)
    client_list = []
#For loop, for each element in the answered list choose element 1 from key IP and element 1 from key MAC
#And store them in a variable called client dict
#Append the clinet dict in the client lists using .append
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

#THis function will print the results
def print_results(result_list):

    print("IP\t\t\tMAC_Address\n-----------------------------------------")
#For loop, for each client in result list, print client IP and client MAC
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_results(scan_result)

#creating arp_header with dst_ip=user_input_ip
#create a ether_header to have Ether frame property with dst_mac = ff:ff:ff:ff:ff:ff
#combine the Ether_header and arp_header to send
#scapy.srp to send the packet in layer2 Ether frame which returns 2 value answered,unanswered timeout=1 specify wait for 1 sec till you getting replay
#declaring a client_list to store a dict values of ip and mac in it nice way of storing a data and use for later use
#declare a client_dict to get ip and mac


# Same version but without comments:

# #!/usr/bin/env python
# import scapy.all as scapy
# import optparse
#
#
# def get_arguments():
#     parser = optparse.OptionParser()
#     parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
#     options, arguments = parser.parse_args()
#     return options
#
# def scan(ip):
#     arp_request = scapy.ARP(pdst=ip)
#     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     arp_request_broadcast = broadcast/arp_request
#     answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
#     clients_list = []
#     for element in answered_list:
#         client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
#         clients_list.append(client_dict)
#     return clients_list
#
# def print_result(results_list):
#     print("IP\t\t\tMAC Address\n-------------------------------------")
#     for client in results_list:
#         print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
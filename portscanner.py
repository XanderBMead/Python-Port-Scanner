import socket
import sys
import ipaddress
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.5)

#Beggining of user input

print("Welcome to my TCP port scanner")
while True:
    try:
        serverIP = input("Input an IP address you would like to scan: ")
        ipaddress.ip_address(serverIP)
        break
    except ValueError:
        print("Invalid IP address")
while True:
    try:
        first = int(input("What is the first port you would like to scan in the range? "))
        break
    except ValueError:
        print("Error: Invalid input. Please enter a number")
    
while True:
    try:
        last = int(input("What is the last port you would like to scan in the range? "))
        break
    except ValueError:
        print("Error: Invalid input. Please enter a number")
while True:
    try:
        timeout = float(input("What would you like to set the timeout to? Default is 0.5 seconds, hit enter to skip ") or 0.5) 
        sock.settimeout(timeout)
        break
    except:      
        if ValueError:
            print("Error: Invalid input. Please enter a number greater than 0")

print("Timeout time set to:", sock.gettimeout())
print("Scanning...", serverIP)

#Start of scan

openlist = []
closedlist = []
openlisttotal = 0
closedlisttotal = 0
noresponse = 0

try:
    for port in range(first,last + 1):  
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((serverIP, port))
        if result == 0:
            print ("Port {}: 	 Open    ".format(port), "Time taken:   ", time.time()-start ,"seconds")
            openlisttotal = openlisttotal + 1
            openlist.append(port)
        elif time.time()-start < timeout:
            print ("Port {}:        Closed    ".format(port), "Time taken:   ", time.time()-start ,"seconds")
            closedlist.append(port)
            closedlisttotal = closedlisttotal + 1
        else:
            print ("Port {}:        Timed out    ".format(port), "Time taken:   ", time.time()-start ,"seconds")
            noresponse = noresponse + 1
        sock.close()

except KeyboardInterrupt:
    print ("You canceled the scan")
    sys.exit()

except socket.error:
    print ("Couldn't connect to the given IP address")
    sys.exit()

if not openlist:
    print("No open ports found")
else:
    print("Open port(s) found: ", openlist)
print("Total: ", openlisttotal)

if not closedlist:
    print("No rejected requests")
else:
    print("Closed port(s) found: ", closedlist)
print("Total: ", closedlisttotal)

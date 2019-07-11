import curses
import sys
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

import socket

# Define who you are talking to (must match ethernet IP and port)
address = ('192.168.1.66', 1000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Set Up the Socket
s.settimeout(1) #only wait 1 second for a resonse



key = ''
player = 'ayyy'
x, y = 2, 20
# https://stackoverflow.com/questions/10693256/how-to-accept-keypress-in-command-line-python
while key != ord('q'):
	key = stdscr.getch()
	stdscr.addstr(y, x, str(key))

	try:
		ret = s.recv(2048) # Read response from footpedal
	except Exception as e:
		ret = e
	stdscr.addstr(y, x, str(ret))

	stdscr.refresh()

curses.endwin()





sys.exit()







# import serial.tools.list_ports
# import glob

# ports = glob.glob('/dev/tty[A-Za-z]*')
# print(ports)

# http://www.toptechboy.com/tutorial/python-with-arduino-lesson-16-simple-client-server-configuration-over-ethernet/
import sys
import curses
import socket

# Define who you are talking to (must match ethernet IP and port)
address = ('192.168.1.66', 1000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Set Up the Socket
s.settimeout(1) #only wait 1 second for a resonse

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

# curses.cbreak()
# curses.noecho()
# stdscr.keypad(1)

# https://stackoverflow.com/questions/10693256/how-to-accept-keypress-in-command-line-python
i = 0
key = ''
while key != ord('q'):
	key = stdscr.getch()

	stdscr.addch(2, 20, i)
	# print(i)
	i += 1
	# try:
	# 	ret = s.recv(2048) # Read response from footpedal
	# 	print(ret)
	# except:
	# 	print('fail')


sys.exit()

import socket
import lxml.etree as ET

def dataParse(data):
	print('parsing')
	xslt = ET.parse('stack13.xsl')
	dom = ET.XML(data)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)
	print(str(newdom))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_addr = ('', 2008)
sock.bind(sock_addr)
sock.listen(40)
print('listening')

print("opening parser.out")

i, j = 0, 0
while True:
	i += 1
	# wait for a connection
	print('asdf')
	connection, client_address = sock.accept()
	while True:
		j += 1
		print(i, j)
		data = connection.recv(8192)
		if data:
			dataParse(data)

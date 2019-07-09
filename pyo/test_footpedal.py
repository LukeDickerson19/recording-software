import sys
import usb


''' NOTES:

	TODO:

		getting this error
			usb.core.USBError: [Errno 16] Resource busy
		when trying to read from device or from endpoint

	Source:

		http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python

	'''



# # find usb device
# f = open('a.csv', 'r')
# devices = []
# for line in f.readlines():
# 	if not line.startswith(' '):
# 		pair = line.split(' ')[2].split(':')
# 		vendor, product = pair[0], pair[1]
# 		devices.append((vendor, product))
# print(devices)
# f.close()



# # find footpedal usb
# # count = 0
# current_devices = usb.core.find(find_all=True)
# for device in current_devices:
# 	print(device)
# 	# pair = str(device).split(' ')[2].split(':')
# 	# vendor, product = pair[0], pair[1]
# 	# if (vendor, product) not in devices:
# 	# 	print(device)
# 	# 	count += 1
# 	# f.write(str(x))
# 	# f.write('\n')
# # print(count)


VENDOR  = 0x0e41
PRODUCT = 0x5055
INTERFACE_NUMBER = 1
device = usb.core.find(idVendor=VENDOR, idProduct=PRODUCT)
print(device)

# must unplug usb and re-plug it for the error
# usb.core.USBError: [Errno 2] Entity not found
# to not appear
device.detach_kernel_driver(INTERFACE_NUMBER)

# config = device.get_active_configuration() 
# INTERFACE_NUMBER = 1
# SETTING = 0
# interface = config[(INTERFACE_NUMBER, SETTING)]

# interface_number = 1 # config[(0,0)].bInterfaceNumber
# print(1)
# alternate_setting = usb.control.get_interface(device, interface_number)
# print(2)
# print(alternate_setting)
# input()
# intf = usb.util.find_descriptor(
# 	config,
# 	bInterfaceNumber = INTERFACE_NUMBER, 
#     bAlternateSetting = interface)
#     # bAlternateSetting = alternate_setting)
# if device.is_kernel_driver_active(0):
#     device.detach_kernel_driver(0)

# cfg = device.get_active_configuration()
# interface_number = cfg[(0,0)].bInterfaceNumber
# print(interface_number)

# print(device)
while True:
	data = device.read(0x82, 16)
	print(data)
	i = input()
	if i == 'q':
		# this got: usb.core.USBError: [Errno 16] Resource busy
		device.attach_kernel_driver(INTERFACE_NUMBER)
		sys.exit()
sys.exit()

# print(device)

# command: "python test_footpedal.py" got an accessed denided error :(
# command: "sudo python test_footpedal.py" didn't work
# commands: "sudo -s" then "python test_footpedal.py" worked!
configuration = device.get_active_configuration()
# print(configuration)

INTERFACE = 1
SETTING   = 0
interface = configuration[(INTERFACE, SETTING)]
# print(interface)
device.detach_kernel_driver(INTERFACE)

ENDPOINT = 0 # OUT = 0, IN = 1
endpoint = interface[ENDPOINT]
print(type(endpoint))
print(endpoint)

while(True):
	data = endpoint.read(16)
	print(data)

sys.exit()





















import pyo
import serial, sys

# # https://github.com/belangeo/pyo/blob/master/pyo/lib/server.py
# pyo.pa_list_devices() # list all audio devices
# print(serial.serial.tools.list_ports.comports())
import serial.tools.list_ports   # import serial module
comPorts = list(serial.tools.list_ports.comports())    # get list of all devices connected through serial port
print(comPorts)
sys.exit()










s = pyo.Server()
s.setInputDevice(4)
s.setOutputDevice(4)
s.boot()
s.start()

print('s.getNchnls() = %s' % s.getNchnls())
# a1 = pyo.Input()
# p1 = pyo.Pan(a1)
# d1 = pyo.Disto(p1, drive=1.0).out()

a2 = pyo.Input(chnl=1)
p2 = pyo.Pan(a2).out(chnl=1)


RECORDING = False
FILENAME = '../files/pyo_recording_test1.wav'

while True:
	user_input = input()
	if user_input == 'q':
		print('Quitting')
		break


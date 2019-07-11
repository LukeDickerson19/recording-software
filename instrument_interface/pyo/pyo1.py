''' NOTES:

	Source:

		http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python

	'''



import pyo
import time, sys

# # https://github.com/belangeo/pyo/blob/master/pyo/lib/server.py
pyo.pa_list_devices() # list all audio devices
sys.exit()


s = pyo.Server()
s.setInputDevice(4)
s.setOutputDevice(4)
s.boot()
s.start()

time.sleep(1) # make sure server is booted

# print('s.getNchnls() = %s' % s.getNchnls())
a1 = pyo.Input()
p1 = pyo.Pan(a1).out()
# d1 = pyo.Disto(p1, drive=0.90).out()

# a2 = pyo.Input(chnl=0)
# p2 = pyo.Pan(a2).out(chnl=1)

# s2 = pyo.Server()
# s2.setInputDevice(0)
# s2.setOutputDevice(4)
# s2.boot()
# s2.start()
# a2 = pyo.Input()
# p2 = pyo.Pan(a2).out()
# # print(s1.getStreams())



RECORDING = False
#FILENAME = '../files/pyo_recording_test1.wav'
FILENAME = '../files/chill_riff2.wav'
# FILENAME = '../files/chill_riff2_with_distortion.wav'

while True:
	user_input = input()
	if user_input == 'r':

		if not RECORDING:
			RECORDING = True
			s.recstart(FILENAME)
			print('Recording to: %s' % FILENAME)
		else:
			RECORDING = False
			s.recstop()
			print('Stopped recording')

	elif user_input == 'q':
		print('Quitting')
		break


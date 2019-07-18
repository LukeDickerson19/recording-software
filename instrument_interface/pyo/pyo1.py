''' NOTES:

	Source:

		http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python

	'''



import pyo
import time, sys
import subprocess

# # https://github.com/belangeo/pyo/blob/master/pyo/lib/server.py
# pyo.pa_list_devices() # list all audio devices
# sys.exit()


s = pyo.Server()
s.setInputDevice(4)
s.setOutputDevice(4)
s.boot()
s.start()

time.sleep(1) # make sure server is booted

# print('s.getNchnls() = %s' % s.getNchnls())
a1 = pyo.Input()
p1 = pyo.Pan(a1).out()
# d1 = pyo.Disto(p1, drive=0.15).out()

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
TMP_FILENAME = '../../files/tmp.wav'
# FILENAME = '../files/chill_riff2_with_distortion.wav'

while True:
	user_input1 = input()
	if user_input1 == 'r':

		if not RECORDING:
			RECORDING = True
			s.recstart(TMP_FILENAME)
			print('Recording ...')
		else:
			RECORDING = False
			s.recstop()
			print('Stopped recording')
			print('Save? y/n')
			user_input2 = input()
			if user_input2 == 'y':
				print('filename?')
				base_filepath = '/'.join(TMP_FILENAME.split('/')[:-1]) + '/'
				print('\t... file will be saved at: ' + base_filepath + '<filename>')
				print('\t... type "exit" to discard recording.')
				user_input3 = input()
				if user_input3 == 'exit':
					cmd = ['rm', TMP_FILENAME]
				else:
					if not user_input3.endswith('.wav'):
						user_input3 += '.wav'
					cmd = ['mv', TMP_FILENAME, base_filepath + user_input3]
				subprocess.run(cmd)

	elif user_input1 == 'q':
		print('Quitting')
		break


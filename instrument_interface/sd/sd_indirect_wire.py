import sounddevice as sd
import numpy as np


''' NOTES:

	TO DO:

		fix it so sound comes from both headphone ears

		figure out what 'data' numpy array represents

	'''


s = sd.Stream(
	device=(4, 0),
	samplerate=44100,
	channels=2)
# s = sd.Stream(
# 	device=(4, 0),
# 	samplerate=44100,
# 	blocksize=1024,
# 	dtype='int16',
# 	latency=None,
# 	channels=2)

# how to use 2 devices
# source: https://github.com/spatialaudio/python-sounddevice/issues/29
# sd.Stream(device=('hw:0,1', 'hw:1,0'), samplerate=(48000, 48000), blocksize=1024, dtype=('int16', 'int16'), latency=None, channels=2):

with s:
	while True:
		data, overflowed = s.read(s.read_available)
		s.write(data)

		# for some reason this doesn't work :(
		#    would have been nice to use it to compare latencies
		#    AttributeError: 'Stream' object has no attribute 'get_input_latency'
		# input_latency  = s.get_input_latency()
		# output_latency = s.get_output_latency()
		# print('input_latency  = %s' % input_latency)
		# print('output_latency = %s' % output_latency)
		# print()


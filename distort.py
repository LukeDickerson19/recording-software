#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.



import sys
import wave
import struct
import math

DEBUG = False

if __name__ == '__main__':

	# Usage: InputFile.wav OutputFile.wav

	buffer = []
	bufferlength = 0
	input_filename  = 'wav2.wav'
	output_filename = 'wav3.wav'

	try:
		drySignal = wave.open(input_filename, 'r')
	except EOFError:
		print("Error: Input file is not a wave file")
		sys.exit()
	except IOError:
		print("Error: File does not exist")
		sys.exit()

	inputParams = drySignal.getparams()

	if inputParams[0:3] != (2, 2, 44100) or inputParams[4:6] != ('NONE', 'not compressed'):
		print("Error: Not a compatible input file")
		print("Input file must be a 2 channel, 16 bit, 44100HZ, uncompressed wave file")
		drySignal.close()
		sys.exit()

	inputLength = drySignal.getnframes()
	print('inputLength = %d' % inputLength)
	completedFrames = 0
	wetSignal = wave.open(output_filename, 'w')
	wetSignal.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

	sample = drySignal.readframes(1)
	print("Distorting...Please Wait")
	while(sample):

		if DEBUG: print('Sample:')
		if DEBUG: print(sample)

		numCH1 = struct.unpack("<hxx", sample)[0]
		numCH2 = struct.unpack("<xxh", sample)[0]

		if DEBUG: print('numCH1 = %s' % numCH1)
		if DEBUG: print('numCH2 = %s' % numCH2)

		# convert to float for division
		floatCH1 = float(numCH1)
		floatCH2 = float(numCH2)

		if DEBUG: print('numCH1 = %s' % numCH1)
		if DEBUG: print('numCH2 = %s' % numCH2)

		# normalize
		normCH1 = floatCH1 / 100
		normCH2 = floatCH2 / 100

		if DEBUG: print('normCH1 = %s' % normCH1)
		if DEBUG: print('normCH2 = %s' % normCH2)

		# compute arctan for distortion
		distCH1 = math.atan(normCH1)
		distCH2 = math.atan(normCH2)

		if DEBUG: print('distCH1 = %s' % distCH1)
		if DEBUG: print('distCH2 = %s' % distCH2)

		# convert back to INT and amplify
		intDistCH1 = int(distCH1 * 1000)
		intDistCH2 = int(distCH2 * 1000)

		if DEBUG: print('intDistCH1 = %s' % intDistCH1)
		if DEBUG: print('intDistCH2 = %s' % intDistCH2)

		# pack into WAVE format
		packCH1 = struct.pack('h' , intDistCH1)
		packCH2 = struct.pack('h', intDistCH2)

		if DEBUG: print('packCH1 = %s' % packCH1)
		if DEBUG: print('packCH2 = %s' % packCH2)

		# output
		buffer.append(packCH1)
		buffer.append(packCH2)
		bufferlength = bufferlength + 1
		# If buffer contains 44100 samples dump buffer to output and display percent complete
		if bufferlength == 44100:
			completedFrames = completedFrames + 44100
			bufferlength = 0
			buffer_str = b''.join(buffer)
			if DEBUG: print('buffer_str = %s' % buffer_str)
			# clear buffer
			del buffer[:]
			wetSignal.writeframes(buffer_str)

			print('%.2f%% completed' % (100 * float(completedFrames) / inputLength))

			# input()

		sample = drySignal.readframes(1)

		# input()

	# dump anything that is still in the buffer before closing
	buffer_str = b''.join(buffer)
	del buffer[:]
	wetSignal.writeframes(buffer_str)

	drySignal.close()
	wetSignal.close()


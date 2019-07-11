''' NOTES:


	Problems:

		only comes through 1 headphone
		can't modify sound at all
			no effects :(

	Description:
		
		PyAudio Example: Make a wire between input and output (i.e., record a
		few samples and play them back immediately).

		This is the callback (non-blocking) version.

	Source:

		https://stackoverflow.com/questions/45905490/playing-soundcard-input-to-soundcard-output-in-python

	'''

import pyaudio
import time

WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

stream = p.open(
	format=p.get_format_from_width(WIDTH),
	channels=CHANNELS,
	rate=RATE,
	input=True,
    input_device_index=4,
	output=True,
	output_device_index=0,
	stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()


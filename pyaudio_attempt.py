import sys, time
import math
import pyaudio
import numpy as np



''' NOTES:

    Problems:

        lag and vibration

    

    Sources:

        get sound coming from input
        https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
        
        get proper input fields???
        https://stackoverflow.com/questions/45039072/how-do-i-use-an-external-microphone-for-pyaudio-instead-of-the-in-built-micropho

        get sound going to output
        https://raspberrypi.stackexchange.com/questions/38756/real-time-audio-input-output-in-python-with-pyaudio

    '''

# used to determine the ID of the input device (input_device_index, for the pyaudio input_stream)
# https://stackoverflow.com/questions/36894315/how-to-select-a-specific-input-device-with-pyaudio
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
# sys.exit()

# used to determine the max input channels of each device
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(i, dev['name'], dev['maxInputChannels'])
sys.exit()



WIDTH = 2
CHUNK = 2**12
RATE = 44100



def note(out_s, freq=440.0, tonelen=0.5, amplitude=5000):
    note = np.sin(
        2*pi*freq * \
        np.linspace(0,tonelen,tonelen*RATE)) * \
    amplitude.astype(int16) # generate sound
    out_s.write(note) # play it



if __name__ == "__main__":

    # open audio channel
    p = pyaudio.PyAudio()
    in_s  = p.open(
        channels=1,
        rate=RATE,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=4)
    out_s = p.open(
        channels=1,
        rate=RATE,
        format=pyaudio.paInt16,
        output=True,
        output_device_index=4)
    
    while True:
        data = np.fromstring(
            in_s.read(
                in_s.get_read_available(),
                exception_on_overflow=False),
            dtype=np.int16)
        out_s.write(data)
        # peak = 2 * np.average(np.abs(data))
        # bars = '#' * int(50 * peak / 2**16)
        # print('%05d %s' % (peak, bars))

    in_s.stop_input_stream()
    in_s.close()
    out_s.stop_stream()
    out_s.close()
    p.terminate()

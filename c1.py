''' NOTES:

    TO DO:

        fix it so sound comes from both headphone ears
            why is the data in the right headphone static?

        plot the left and right head phones over time 
        make the axes show the duration over time
            (maybe a second)

        the frequency chart

        maybe make a backup of all this first

        figure out what 'data' numpy array represents
            plot (net) volume over time
            frequency
                make each frequency appear on a plot that has
                    frequency on the y axis

                see spectrogram.py

    '''


import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

SAMPLERATE = 44100
WINDOW = 200
DOWNSAMPLE = 10
INTERVAL = 30
CHANNELS = [1]
length = int(WINDOW * SAMPLERATE / (1000 * DOWNSAMPLE))
plotdata = np.zeros((length, len(CHANNELS)))



mapping = [c - 1 for c in CHANNELS]  # Channel numbers start with 1
q = queue.Queue()

wav2 = 'wav2.wav'
all_data = np.array([[0.0, 0.0]])

# def audio_callback(indata, frames, time, status):
def audio_callback(indata, outdata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""

    # outdata[:] = indata  # this wires input directly into output
    # for some reason the right headphone data is just a bunch of static
    # so I copied the left headphone data (which is good) into the right
    outdata[:] = 10 * np.repeat(indata[:,0][:,np.newaxis], 2, 1)

    # print('outdata')
    # print(outdata.shape)
    # print(outdata)

    # # used to verify outdata still has same precision indata has
    # print(np.format_float_scientific(outdata[0][0], unique=False, precision=15))

    # global all_data
    # all_data = np.concatenate((all_data, outdata))
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(outdata[::DOWNSAMPLE, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        # print(data.shape)
        # print(data)
        # print()
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


s = sd.Stream(
    device=(4, 4),
    samplerate=SAMPLERATE,
    channels=2,
    callback=audio_callback)

fig, ax = plt.subplots()
lines = ax.plot(plotdata)
ax.set_ylim((-0.5, 0.5))
ax.yaxis.grid(True)
ani = FuncAnimation(fig, update_plot, interval=INTERVAL, blit=True)

with s:
    plt.show()

import soundfile as sf
# for i in range(all_data.shape[0]):
#     print(all_data[i])

sf.write(wav2, all_data, SAMPLERATE)

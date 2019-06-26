''' NOTES:

    TO DO:

        NOW:

            get distortion effect
                https://www.hackaudio.com/digital-signal-processing/distortion-effects/
                http://sites.music.columbia.edu/cmc/music-dsp/FAQs/guitar_distortion_FAQ.html
                https://ccrma.stanford.edu/~jos/pasp05/Nonlinear_Distortion.html
                http://people.math.sfu.ca/~cbm/aands/

            fix it so sound comes from both headphone ears
                why is the data in the right headphone static?

            plot the left and right head phones over time
            make the axes show the duration over time
                (maybe a second)

            the frequency chart (aka spectrogram)

            maybe make a backup of all this first

            figure out what 'data' numpy array represents
                plot (net) volume over time
                frequency
                    make each frequency appear on a plot that has
                        frequency on the y axis

                    see spectrogram.py

        LONG TERM:

            set up pedal


    THOUGHTS:

        I'm worried that:

            when I try to create/copy-in effects for this
            it will increase the latency to much
                does numpy use C in its backend?

            it won't be able to record 2 inputs and output them simulatniously

        It would be cool to create an effect like the piano pedal where you can hold it down
        and whatever notes are played when its held down are elongated even when you stop
        holding the note

        It would be cool if the Program could figure out what time signature you're playing
        in by simply listening to you play
            as a musician your time signature is going to fluctuate slightly ...
            and you could set it to either

        It would be cool if you could pre-set the algorithm to apply various
        effects at various points in the song (identified with AI)

    '''


import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=10)
import sounddevice as sd
sd.default.latency = 'low'
plotdata = np.zeros(128)

SAMPLERATE = 44100
WINDOW = 200
DOWNSAMPLE = 10
INTERVAL = 30
CHANNELS = [1]
length = int(WINDOW * SAMPLERATE / (1000 * DOWNSAMPLE))
# print(plotdata)
# print(plotdata.shape)
# sys.exit()


# mapping = [c - 1 for c in CHANNELS]  # Channel numbers start with 1
q = queue.Queue()

wav2 = 'wav2.wav'
all_data = np.array([[0.0, 0.0]])

cubic = lambda x : x - (1/3)*(x**3)
alpha = 75
arctan = lambda x : (2 / np.pi) * np.arctan(alpha * x)
# 2 / pi * arctan(alpha*input)

# def audio_callback(indata, frames, time, status):
def audio_callback(indata, outdata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""

    # outdata[:] = indata  # this wires input directly into output
    # for some reason the right headphone data is just a bunch of static
    # so I copied the left headphone data (which is good) into the right

    # print(indata[:,0])

    # clean
    # outdata[:] = 10 * np.repeat(indata[:,0][:,np.newaxis], 2, 1)

    # distortion:
    # full wave rectifier
    # "negative values are set to their positive equivalent" (paraphrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # outdata[:] = 10 * np.repeat(np.absolute(indata[:,0])[:,np.newaxis], 2, 1)

    # half wave rectifier
    # "negative values are set to zero" (paraphrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # https://stackoverflow.com/questions/3391843/how-to-transform-negative-elements-to-zero-without-a-loop
    # outdata[:] = 10 * np.repeat(np.clip(indata[:,0], a_min=0, a_max=None)[:,np.newaxis], 2, 1)

    # infinite clipping
    # "all positive values are set to the maximum value, and all negative values are set to the minimum value." (para-phrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/infinite-clipping/
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
    # outdata[:] = 0.05 * np.repeat(np.where(indata[:,0][:,np.newaxis] > 0, 1.0, -1.0), 2, 1)

    # hard clipping
    # "if signal goes above max, its set to max; it if goes below min, its set to min" (paraphrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/hard-clipping/
    # this will propably give a clean sound when nothing is being played
    amplitude = 500.0
    threshold = 0.0005
    outdata[:] = amplitude * \
        np.repeat(
            np.clip(
                indata[:,0][:,np.newaxis],
                a_min=-threshold, a_max=threshold),
            2, 1)
    # print(outdata[:,0][:,np.newaxis].shape)

    # soft clipping
    # "same as hard clippling but with smooth curve instead" (paraphrased)
    # cubic fuction:    output = input - (1 / 3)*input^3
    # arc tan function: output = 2 / pi * arctan(alpha*input)
    #     "alpha" values typically range from 1 to 10. If alpha is way more than 10, softclippling approaches infinite clipping
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/soft-clipping/
    # amplitude = 10.0
    # left_indata = indata[:,0][:,np.newaxis]
    # # # print(f(left_indata))
    # outdata[:] = amplitude * \
    #     np.repeat(
    #         # cubic(left_indata),
    #         arctan(left_indata),
    #         2, 1)


    # bit crushing
    # "round signal to -1, 0, or 1 (or any combo you want)" (para-phrased)
    #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/bit-crushing/



    # print('outdata')
    # print(outdata.shape)
    # print(outdata)

    # # recording eventually gets laggy this way
    # global all_data
    # all_data = np.concatenate((all_data, outdata))

    # # used to verify outdata still has same precision indata has
    # print(np.format_float_scientific(outdata[0][0], unique=False, precision=15))

    # global all_data
    # all_data = np.concatenate((all_data, outdata))
    # Fancy indexing with mapping creates a (necessary!) copy:
    # q.put(outdata[::DOWNSAMPLE, mapping])
    q.put(outdata[:,0][:,np.newaxis])

def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    # global plotdata
    # while True:
    #     try:
    #         data = q.get_nowait()
    #     except queue.Empty:
    #         break
    #     # print(data.shape)
    #     # print(data)
    #     # print()

    #     # shift = len(data)
    #     # plotdata = np.roll(plotdata, -shift, axis=0)
    #     # plotdata[-shift:, :] = data

    #     plotdata = data
    # for column, line in enumerate(lines):
    #     # line.set_ydata(plotdata[:, column])
    #     line.set_ydata(plotdata)
    plotdata = q.get_nowait()
    for column, line in enumerate(lines):
        line.set_ydata(plotdata)
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
sf.write(wav2, all_data, SAMPLERATE)

open('txt2.txt', 'w').close()
f = open('txt2.txt', 'w')
for i, v in enumerate(all_data):
    f.write('%s\n' % v)
    if i > 100:
        break

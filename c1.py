''' NOTES:

    TO DO:

        NOW:

            test bit_crushing

            rename a,b,c:1,2 files to make more sense

            put distortion options outside of callback function

            update backup

            push it all to github

            find a way to record
                that doesn't create lag over time
                np.concatinate() didn't work
                vvv    this explains why    vvv
                https://stackoverflow.com/questions/38470264/numpy-concatenate-is-slow-any-alternative-approach
                its because its copying over the whole array each time
                    in what other senarios is numpy copying shit unneccessarily?
                try a python list.append()
                if that doesn't work (or affets latency in any noticable way) use a linked list



        LONG TERM:


            set up pedal
                probably just need to create another InputStream w/ sounddevice with a callback function (does InputStream have a callback function? If not, gotta find some way to access the raw data)
                In the callback function (or whatever data stream) there will be a boolean thats constantly being updated, find a way to interpret that to set another global boolean to turn distortion on/off


            setup 2i2 to work with a mic and a guitar
                why does it say the 2i2 only has 2 channels? shouldn't it be 4?

                for now just use computer's mic (and create a 2nd sd.Stream)


            right now sd.default.latency = 'low' in order to decrease latency.

                found here: https://stackoverflow.com/questions/39990274/too-high-latency-while-trying-to-manipulate-sound-arrays-using-sounddevice-in-py

                it does this by decreasing the length of the numpy array 'indata' (from 512 to 128)
                which decreases the quality of the sound (idk why)

                I want to find a way to decrease latency without decreasing sound quality as much.
                Possible solutions are:

                    use:
                        multiprocessing or async-io to do more shit in parallel hopefully
                            https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io

                        research sd.default.latency (maybe theres a way to set it to 'medium low' or something to put it at 256, maybe 256 wont have noticable latency and quality will be pretty good too)

                        maybe it could just do linear interpolation of the 128 indata and put it back to 512 (or 1024 lol XD)
                            or maybe something smoother than linear interpolation


            make basic frequency chart (aka spectrogram)
                no Key interpretation
                see spectrogram.py


            figure out what 'indata' numpy array represents
                create a new script thats just an OutputStream (to headphones)
                create numpy arrays that are a sine wave with specific note's freqency (middle C)
                plot it over time
                see if the pitch in the headphones matches the pitch on your guitar (don't forget to tune it)
                dig into spectogram.py to figure out how it determines frequency value


            figure out why right headphone data is just static
                right now the hack is simply to copy the left-headphone data into the right
                however from testing it by downloading classical_music.wav files from online
                and playing it through the headphones and outputting the data to the console,
                its clear the data should not be the same in both head phones

                perhaps plot the left and right data on the same plot (one line red, one line blue)
                and see their difference, maybe they're not that different and you just need to
                randomly change the right one a bit from the left to get rid of that chorus sound


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
            and you could set it to either go with it (because maybe you want the song to speed up or slow down)
            or you could tell it to stick with whatever time signature it first identified (to keep you the musician on track)

            it would be nice if this was then played back in the headphones or displayed with a blinking light on the pedal or with some display on the computer screen

            this could be useful for
            having the computer properly time the switch from 1 effect to another (triggered with foot pedal), thus allowing the musician to press the pedal slightly before the

        It would be cool if it could Identify what key you are playing in and
        display horizontal lines on the screen for each note in the key
            and when you stop playing the lines go away

            ... having horizontal and vertical lines (for key and time sig. respectivewly) appear on a black screen when you start playing and disappearing when you stop would be dope!!!!

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
# print(plotdata)
# print(plotdata.shape)
# sys.exit()

SAMPLERATE = 44100


# mapping = [c - 1 for c in CHANNELS]  # Channel numbers start with 1
q = queue.Queue()

wav2 = 'wav2.wav'
all_data = np.array([[0.0, 0.0]])

cubic = lambda x : x - (1/3)*(x**3)

alpha = 75
arctan = lambda x : (2 / np.pi) * np.arctan(alpha * x)

threshold = 0.0005
bit_crushing = lambda x : threshold if x > threshold else (-threshold if x < -threshold else 0)

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
    amplitude = 500.0
    left_indata = indata[:,0][:,np.newaxis]
    outdata[:] = amplitude * \
        np.repeat(
            bit_crushing(
                left_indata),
            2, 1)

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

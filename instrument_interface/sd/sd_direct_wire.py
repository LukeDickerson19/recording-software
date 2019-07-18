import re, sys
import subprocess
# device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []
l = str(df).split('\\n')
for a in l:
    print(a + '\n')
    print()

# # trying to figure out how to input ethernet input
# for i in str(df).split('\n'):
#     print('start')
#     print(i)
#     print('end')
#     print()
#     if i:
#         info = device_re.match(i)
#         if info:
#             dinfo = info.groupdict()
#             dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
#             devices.append(dinfo)
# print(devices)
# sys.exit()



























import queue
import sys
import timeit

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

RECORDING = False


# mapping = [c - 1 for c in CHANNELS]  # Channel numbers start with 1
q = queue.Queue()

# used for recording all the data
# all_data = np.array([[0.0, 0.0]])
all_data = []

cubic = lambda x : x - (1/3)*(x**3)

alpha = 5000
arctan = lambda x : (2 / np.pi) * np.arctan(alpha * x)

# https://dsp.stackexchange.com/questions/13142/digital-distortion-effect-algorithm
f = lambda x : \
    np.where(
        x > 0,
        1.0 - np.exp(-x),
        -1.0 + np.exp(x))

# def audio_callback(indata, frames, time, status):
def audio_callback(indata, outdata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""

    # outdata[:] = indata  # this wires input directly into output
    # for some reason the right headphone data is just a bunch of static
    # so I copied the left headphone data (which is good) into the right

    # # clean:
    # outdata[:] = 10 * np.repeat(indata[:,0][:,np.newaxis], 2, 1)


    # # distortion effects:

    # # full wave rectifier
    # # "negative values are set to their positive equivalent" (paraphrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # outdata[:] = 10 * np.repeat(np.absolute(indata[:,0])[:,np.newaxis], 2, 1)

    # # half wave rectifier
    # # "negative values are set to zero" (paraphrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/full-wave-rectification/
    # # https://stackoverflow.com/questions/3391843/how-to-transform-negative-elements-to-zero-without-a-loop
    # outdata[:] = 10 * np.repeat(np.clip(indata[:,0], a_min=0, a_max=None)[:,np.newaxis], 2, 1)

    # # infinite clipping
    # # "all positive values are set to the maximum value, and all negative values are set to the minimum value." (para-phrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/infinite-clipping/
    # # https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
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
                indata[:,0],
                a_min=-threshold,
                a_max=threshold,
                out=indata[:,0])[:,np.newaxis],
            2, 1)
    # print(outdata[:,0][:,np.newaxis].shape)

    # # soft clipping
    # # "same as hard clippling but with smooth curve instead" (paraphrased)
    # # cubic fuction:    output = input - (1 / 3)*input^3
    # # arc tan function: output = 2 / pi * arctan(alpha*input)
    # #     "alpha" values typically range from 1 to 10. If alpha is way more than 10, softclippling approaches infinite clipping
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/soft-clipping/
    # amplitude = 100.0
    # left_indata = indata[:,0][:,np.newaxis]
    # outdata[:] = amplitude * \
    #     np.repeat(
    #         # cubic(left_indata),
    #         # arctan(left_indata),
    #         f(left_indata),
    #         2, 1)


    # # bit crushing
    # # "round signal to -1, 0, or 1 (or any combo you want)" (para-phrased)
    # #    - https://www.hackaudio.com/digital-signal-processing/distortion-effects/bit-crushing/
    # amplitude = 100.0
    # threshold = 0.0005
    # left_indata = indata[:,0][:,np.newaxis]
    # hard_clipping = np.clip(left_indata, a_min=-threshold, a_max=threshold)
    # in_range = np.logical_and(-threshold < hard_clipping, hard_clipping < threshold)
    # outdata[:] = amplitude * \
    #     np.repeat(
    #         # 10 * (10e6 * left_indata).astype(int) / 10e7,
    #         np.where(
    #             in_range,
    #             0, hard_clipping),
    #         2, 1)
    # # print(outdata[:,0][:,np.newaxis].shape)

    if RECORDING:
        all_data.append(outdata.copy())

    # print('outdata')
    # print(outdata.shape)
    # print(outdata)

    # # used to verify outdata still has same precision indata has
    # print(np.format_float_scientific(outdata[0][0], unique=False, precision=15))

    # # Fancy indexing with mapping creates a (necessary!) copy:
    # # q.put(outdata[::DOWNSAMPLE, mapping])
    # q.put(outdata[:,0][:,np.newaxis])

# def update_plot(frame):
#     """This is called by matplotlib for each plot update.

#     Typically, audio callbacks happen more frequently than plot updates,
#     therefore the queue tends to contain multiple blocks of audio data.

#     """
#     # global plotdata
#     # while True:
#     #     try:
#     #         data = q.get_nowait()
#     #     except queue.Empty:
#     #         break
#     #     # print(data.shape)
#     #     # print(data)
#     #     # print()

#     #     # shift = len(data)
#     #     # plotdata = np.roll(plotdata, -shift, axis=0)
#     #     # plotdata[-shift:, :] = data

#     #     plotdata = data
#     # for column, line in enumerate(lines):
#     #     # line.set_ydata(plotdata[:, column])
#     #     line.set_ydata(plotdata)
#     plotdata = q.get_nowait()

#     # print(outdata.shape)

#     # recording eventually gets laggy this way
#     # global all_data
#     # all_data = np.concatenate((all_data, outdata))
#     # all_data += outdata.tolist()
#     # print(len(all_data))


#     for column, line in enumerate(lines):
#         line.set_ydata(plotdata)
#     return lines

s = sd.Stream(
    device=(4, 4),
    samplerate=SAMPLERATE,
    channels=2,
    callback=audio_callback)

# fig, ax = plt.subplots()
# lines = ax.plot(plotdata)
# # ax.set_ylim((-10.0, 10.0))
# ax.set_ylim((-0.5, 0.5))
# ax.yaxis.grid(True)
# ani = FuncAnimation(fig, update_plot, interval=50, blit=True)

with s:
    input()
    # plt.show()
    # while True:
    #     user_input = input()
    #     if user_input == 'r':
    #         if RECORDING:
    #             RECORDING = False
    #         else:
    #             all_data = []
    #             RECORDING = True
    #     if user_input == 'p':
    #         if PLAYING:
    #             PLAYING = False

# save recorded data to .wav and .txt files
if RECORDING:

    all_data = 20 * np.reshape(
        all_data,
        (len(all_data)*len(all_data[0]), 2))
    wav2 = 'cool_riff2.wav'
    import soundfile as sf
    sf.write(wav2, all_data, SAMPLERATE)

    fn = 'txt2.txt'  # this is just to compare .wav to raw numpy array
    open(fn, 'w').close() # clear file
    f = open(fn, 'w')
    for i, v in enumerate(all_data):
        f.write('%s\n' % v)
        if i > 100:
            break




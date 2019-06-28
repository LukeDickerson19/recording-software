#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import argparse
import tempfile
import queue
import sys

import sounddevice as sd
sd.default.latency = 'low'

import soundfile as sf
import numpy as np
assert np

SR = 44100
amplitude = 500.0
threshold = 0.0005



''' NOTES:

    DESCRIPTION:

        the record_unlimited() function allows to to record for an unlimited amount of time

        if save_file_path is specified it will save the file to that path

    SOURCE:

        this code:
        https://python-sounddevice.readthedocs.io/en/0.3.12/examples.html

    '''

def record_unlimited(filename=None):

    q = queue.Queue()

    def callback(indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""

        outdata[:] = amplitude * \
            np.repeat(
                np.clip(
                    indata[:,0][:,np.newaxis],
                    a_min=-threshold,
                    a_max=threshold,
                    out=indata[:,0][:,np.newaxis]),
                2, 1)
        # outdata[:] = 1 * np.repeat(indata[:,0][:,np.newaxis], 2, 1)
        # q.put(indata.copy())
        q.put(outdata[:,0][:,np.newaxis].copy())

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(
        filename,
        mode='w+',
        samplerate=SR,
        channels=1) as file:

        with sd.Stream(
            samplerate=SR,
            device=(4, 4),
            channels=2,
            callback=callback):

            i = 0
            while True:
                file.write(100 * q.get())
                print('wrote to file %d' % i)
                i += 1

record_unlimited('wav4.wav')
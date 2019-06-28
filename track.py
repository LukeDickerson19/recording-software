import os, shutil
import sounddevice as sd
from rec_unlimited import record_unlimited
from other_useful_functions import *
from constants import *





class Track(object):

    def __init__(self, name):
        self.audio = None
        self.name  = name
        self.muted = False

    def empty(self):
        return self.audio is None

    def record(self, duration=None):
        if duration is None:
            record_unlimited()
        else:
            pass

    def clear(self):
        self.audio = None

    def save(self, path):

        path += '/' + name

        # create directory with this tracks name
        os.mkdir(path)

        # save audio data

    def open(self, path):
        successfully_opened = False
        try:
            track = Track()
            # get audio data from path
            successfully_opened = True
        except:
            pass
        return track, successfully_opened

    def pprint(self):
        pprint(self.name)

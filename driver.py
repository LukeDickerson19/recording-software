import os, shutil
import sounddevice as sd
from rec_unlimited import record_unlimited
from other_useful_functions import *
from constants import *


''' NOTES

    TO DO:

        make it so you can save a recording file in rec_unlimited

        change record unlimited to have a different key board command so the program doesnt end
        when you finish a recording

        create play/pause commands




    DESCRIPTION

        This script allows you to record a track and then
        record another track over top of it. A simple FUCKING
        task that recording software and recording apps, either
        don't offer, or always have issues trying.

    USAGE:
    
        run program with driver.py

        press r to record
        press r again to stop recording
        press p to play
        press p again to pause
        press s to save the recordings
        press t then enter a time to specify which second (float) to put the cursor at (t then hitting enter and typing no time puts it at the beginning)
        press o to open a recording


        press h for help

    SOURCES:

        sounddevice - used to record audio with python
        https://python-sounddevice.readthedocs.io/en/0.3.12/

            questions:

                Q: how do i start recording?
                A:
                    duration = 10.5  # seconds
                    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)

                    Q: What is channels?
                    A: 

                Q: how do i stop recording?
                A:

                Q: how do i play a recording?
                A: 

    IDEAS:

        long term:
            this becomes a web app that you can both access from the web
            or download and install on your computer

            it has ads for the free version
            it has no ads for the pro version (paid)
            the pro version has:
                sound cloud, spotify, etc analytics
                    analytics look at:
                        how many people are listening to your music
                        what other songs are people listening to with your music?
                        of the other musicians that make music with a similar audience what shows are they performing at?
                            of those shows which of those do you as a musician have a change of performing at if you apply?
                                shows credentials of musician that applied who did and did not
                                    credentials include:
                                        number of listeners on spotify, soundcloud, etc


    '''

DEFAULT_RECORD_PATH = './recordings/'


def valid_path(path):
    return os.path.exists(path)


def valid_file_name(name):
    return not any([c == '/' for c in name])


class Recording(object):

    def __init__(self, name=None, path=None):
        self.tracks = []
        self.name = name
        self.path = path
        self.t = 0.0
        self.playing = False

    # create a track (w/ or w/out a specific name)
    def create_track(self, name=None):
        track = Track(name if name else 'track%d' % len(self.tracks))
        self.tracks.append(track)
        return track

    # remove the track specified with 'name'
    def remove_track(self, name):
        track_found = False
        for track in self.tracks:
            if track.name == name:
                track_found = True
                self.tracks.remove(track)
                break
        if not track_found:
            pprint('Track \'%s\'not found' % name)

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    # change this recordings name (both in this program and this
    # recording's file name if its been saved)
    def rename(name):
        self.name = name
        if self.saved:
            os.renames(self.path + '/' + self.name, self.path + '/' + name)

    # save/create a directory with this recording's name at self.path
    # save/create each track in this recording
    def save(self):

        # get location to save to
        while not self.path:
            pprint('type path to save to')
            pprint('or press enter for DEFAULT_RECORD_PATH: %s' % DEFAULT_RECORD_PATH)
            pprint('or type CANCEL to cancel saving')
            user_input = input()
            if user_input == 'CANCEL':
                return
            elif valid_path(user_input):
                self.path = user_input
            else:
                pprint('path \'%s\' does not exist' % user_input)

        # get name to save with
        while not self.name:
            pprint('type name to save recording with')
            pprint('or type CANCEL to cancel saving')
            user_input = input()
            if user_input == 'CANCEL':
                return
            elif valid_file_name(user_input):
                self.name = user_input
            else:
                pprint('invalid file name: \'%s\'' % user_input)

        path = self.path + '/' + self.name

        # create a directory with this recordings name if it doesn't exist yet
        if not self.saved():
            os.mkdir(path)
        else:
            # delete all contents of this recording's directory
            self.delete(path=path)

        # save each track
        for track in self.tracks:
            track.save(path)

    # create a new directory
    def saveas(self, name=None, path=None):
        if name is None and path is None:
            pprint('save as requires to specify a different name or a different path')
            return

        name = self.name if name is None else name
        path = self.path if path is None else path

        self.save(name=name, path=path) 

    # return True/False if this recording has been saved yet
    def saved(self):
        return any([dir_name == self.name for dir_name in os.listdir(self.path)])

    # open recording from file
    # @staticmethod
    def open():

        recording_opened = False
        while not recording_opened:
            pprint('type path of recording to open')
            pprint('or press enter for DEFAULT_RECORD_PATH: %s' % DEFAULT_RECORD_PATH)
            pprint('or type CANCEL to cancel opening')
            user_input = input()
            if user_input == 'CANCEL':
                break
            else:
                path = None
                if user_input == '':
                    path = DEFAULT_RECORD_PATH
                elif valid_path(user_input):
                    path = user_input
                else:
                    pprint('path \'%s\' does not exist' % user_input)
                if path:
                    pprint('Select the recording to open by')
                    pprint('typing the number in front of it')
                    num_recordings = 0
                    for i, d in enumerate(next(os.walk(path))[1]):
                        pprint('%d\t%s' % ((i + 1), d))
                        num_recordings += 1
                    while True:
                        try:
                            user_input = int(input()) - 1
                            if 0 <= user_input <= num_recordings - 1:
                                selected_recording = list(next(os.walk(path))[1])[user_input]
                                if path[-1] is not '/':
                                    path += '/'
                                path += selected_recording
                                break
                            else:
                                pprint('pick a number 1 through %d you fucking idiot' % num_recordings)
                                raise Exception
                        except:
                            pprint('invalid input')

                    successfully_opened = False
                    try:
                        recording = Recording(
                            name=selected_recording,
                            path=path[:-len(selected_recording)])
                        for track_dir in os.listdir(path):
                            track = Track.open_form_file(path + '/' + track_dir)
                            recording.tracks.append(track)
                        successfully_opened = True
                        pprint('Opened Recording')
                        recording.pprint()
                    except:
                        pprint('Failed to open recording at: %s' % path)
                    return recording

    # delete this recording object in the program and all saved data
    def delete(self, path=None):
        if self.saved():
            shutil.rmtree(self.path if not path else path)

    def pprint(self):
        pprint('Name:\t%s' % self.name)
        pprint('Path:\t%s' % self.path)
        pprint('Tracks:')
        if self.tracks:
            for track in self.tracks:
                track.pprint()
        else:
            pprint('no tracks')

class Track(object):

    def __init__(self, name):
        self.audio = None
        self.name = name
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


if __name__ == '__main__':

    recording = None
    path = DEFAULT_RECORD_PATH

    while True:

        user_input = input()

        if user_input == 'r':
            if recording is None:
                recording = Recording()
            track = recording.create_track()
            track.record()

        elif user_input == 'p':
            if recording.playing:
                recording.play()
            else:
                recording.pause()
        elif user_input == 's':
            recording.save()
        elif user_input == 't':
            user_input = input()
            recording = 0.0 if user_input == '' else float(user_input)
        elif user_input == 'o':
            recording = Recording.open()

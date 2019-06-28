import os, shutil
import sounddevice as sd
from rec_unlimited import record_unlimited
from other_useful_functions import *
from constants import *
from track import Track
from recording import Recording


''' NOTES

    TO DO:

        perhaps this could lead to a Audio Software Engineer position w/ Warner Music
            Do they have those positions?
            Do they allow you to work remotely?

        upgrade to newer version:
            python3 -m pip install sounddevice --upgrade
                source: https://python-sounddevice.readthedocs.io/en/0.3.13/installation.html

        check these out:
            https://realpython.com/playing-and-recording-sound-python/

            https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
                found from here: https://stackoverflow.com/questions/48653745/continuesly-streaming-audio-signal-real-time-infinitely-python

            guitar effects in python!
            http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python
            https://github.com/Souloist/audio-effects
                this one uses pyaudio!
                ... but does it have Distortion, and can you make custom effects?

            questions:
                how do you stop the record_unlimited() function?
                does pyaudio allow simultanious recording and playback?

        make it so you can save a recording file in rec_unlimited


        change record unlimited to have a different key board command so the program doesnt end
        when you finish a recording

        create play/pause commands

        make it so each track and recording has a notes section




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
        https://python-sounddevice.readthedocs.io/en/0.3.13/

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



def valid_path(path):
    return os.path.exists(path)


def valid_file_name(name):
    return not any([c == '/' for c in name])





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

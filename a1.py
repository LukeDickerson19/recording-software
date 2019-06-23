''' NOTES:

	Source:

		http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python

	'''



import pyo

s = pyo.Server(audio='jack', nchnls=1).boot()
s.start()

a = pyo.Input(chnl=0)
chorus = pyo.Chorus(a, depth=.5, feedback=0.5, bal=0.5).out()

s.gui()

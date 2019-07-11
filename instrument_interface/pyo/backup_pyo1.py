''' NOTES:

	Source:

		http://www.matthieuamiguet.ch/blog/diy-guitar-effects-python

	'''



import pyo

# # https://github.com/belangeo/pyo/blob/master/pyo/lib/server.py
# pyo.pa_list_devices() # list all audio devices

s = pyo.Server()
s.setInputDevice(4)
s.setOutputDevice(4)
s.boot()
s.start()

a = pyo.Input()
p = pyo.Pan(a).out()
# d = pyo.Disto(p, drive=1.0).out()

input()

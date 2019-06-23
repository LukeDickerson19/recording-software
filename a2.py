# import pyo

# s = pyo.Server()
# s.boot()
# s.setInputDevice(4)
# s.setOutputDevice(0)
# s.start()

# a = pyo.Input(chnl=0)
# chorus = pyo.Chorus(a, depth=.5, feedback=0.5, bal=0.5).out()



from pyo import *


# s = Server()
# s.setInputDevice(0)
# s.setOutputDevice(0)
# s.boot()
# s.start()




print(1)
s = Server(nchnls=2)
print(2)
s.boot()
print(3)
s.start()
print(4)
wav = SquareTable()
env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
met = Metro(.125, 12).play()
amp = TrigEnv(met, table=env, dur=1, mul=.1)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
out = Osc(table=wav, freq=pit, mul=amp).out()



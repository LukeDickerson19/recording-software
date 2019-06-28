import sounddevice as sd
sd.default.latency = 'low'
sd.default.device = 4
sd.default.channels = 2
fs = 44100
sd.default.samplerate = fs

duration = 5
print(1)
myrecording = sd.rec(int(duration * fs))
print(2)
sd.wait()
print(3)
print(myrecording)
print(4)
sd.play(myrecording)
input()
print(5)
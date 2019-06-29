import numpy as np
np.set_printoptions(threshold=10)
import soundfile as sf
import sounddevice as sd
sd.default.latency = 'low'

# filename = 'wav2.wav'
filename = 'cool_riff1.wav'
# filename = 'classical_music.wav'
# filename = 'classical_music2.wav'

# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='float32')

print('fs:')
print(type(fs))
print(fs)

print('data:')
print(type(data))
print(data.shape)
np.set_printoptions(threshold=100)

i = 0
n = 95
def callback(outdata, frames, time, status):
	global i, n
	print(data[i:i+n].shape)
	outdata[:] = data[i:i+n] / 20.0
	i += n


with sd.OutputStream(
	samplerate=fs,
    device=4,
    channels=2,
    callback=callback):
	input()

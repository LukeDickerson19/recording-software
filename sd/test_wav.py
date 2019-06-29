import sys
import sounddevice as sd
import soundfile as sf
import numpy as np
np.set_printoptions(threshold=sys.maxsize)


filename = 'wav2.wav'
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
# for row in data:
# 	print(row)

# sf.write('classical_music2.wav', data, fs)

# # this was originally here to test if copying the left
# # data into the right data could make sounds come from
# # both head phones
# if filename == 'wav2.wav':
# 	for i in range(data.shape[0]):
# 		left, right = data[i][0], data[i][1]
# 		data[i][1] = data[i][0]
# 		# data[i][1] = left if left != 0 and right == 0 else 1e3 * right
# 		# left, right = data[i][0], data[i][1]
# 		# # print(left, right)

# if filename == 'classical_music.wav':
# 	for i in range(data.shape[0]):
# 		# left, right = data[i][0], data[i][1]
# 		data[i][0] /= 10
# 		data[i][1] /= 10

sd.play(data, fs, device=4)


status = sd.wait()  # Wait until file is done playing
import time, os

# print("sample text", end='\r', flush=True)
print('start')
for i in range(15)[::-1]:
    print('    %d ' % i, end='\r', flush=True)
    time.sleep(.25)
print('\nend')



import numpy as np
from matplotlib import pyplot as plt

f = open('{}'.format('./Kramers-Kronig.txt'), 'r')
x_axis = []
spectra = []
x_tick =[]
i = 0
for line in f:
    i = i + 1
    line = line.strip().split('\t')
    x_axis.append(line[0])
    spectra.append(line[1])
    if i % 10 == 1:
        x_tick.append((line[0]))
print(x_axis)
x = np.array(x_tick, np.complex_)
xi = list(range(len(x)))
spectra = np.array(spectra, np.float32)
x_axis = np.array(x_axis, np.complex_)
font = {'size': 8}
plt.rc('font', **font)
plt.plot(x_axis, spectra)
plt.xticks(x, x_tick, size='small')
plt.show()
plt.pause(20)

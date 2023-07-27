import numpy
import numpy.fft
f = open('{}'.format('Kramers-Kronig.txt'), 'r')
x_axis = []
spectra = []
for line in f:
    line = line.strip().split('\t')
    x_axis.append((line[0]))
    spectra.append(line[1])

kk.fft.pure2kk(spectra, n=None, axis=-1)


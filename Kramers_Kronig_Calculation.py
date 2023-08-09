import math
import scipy.integrate
import numpy as np


def kkr(de, eps_imag, cshift):
    f = open('{}'.format(eps_imag), 'r')
    x_axis = []
    spectra = []
    for line in f:
        line = line.strip().split('\t')
        x_axis.append((line[0]))
        spectra.append(line[1])
    eps_imag = np.array(spectra)
    nedos = eps_imag.shape[0]
    eps_real = []

    for i_r in range(nedos):
        w_r = de * i_r
        total = np.zeros(eps_imag.shape[1:], dtype=np.complex_)

        for i_i in range(nedos):
            w_i = de * i_i
            a = float(eps_imag[i_i])
            val = a * ((1 / (w_r - w_i - complex(0, cshift)))
                       + (1 / (- w_r - w_i + complex(0, cshift)))) * (-0.5)
            total = total + val
        eps_real.append(total * (2 / math.pi) * de + np.diag([1, 1, 1]))
    return np.real(np.array(eps_real))

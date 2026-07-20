# Use the following script to calculate the median value of LOS acceleration magnitude, total mass median with errors and SNR for maxL params

import numpy as np
import pandas as pd
from pathlib import Path
import h5py
from pycbc.conversions import snr_from_loglr

h = h5py.File("posterior_extract.hdf", "r")
mag_acc = h['samples']["acc_mag"][:]

m1 = h['samples']["mass1"][:]
m2 = h['samples']["mass2"][:]
m_total = m1 + m2

print("mag_acc_90", np.percentile(mag_acc, 90))
print("M_total", np.median(m_total))
print("M_total_90_low", np.percentile(m_total, 5))
print("M_total_90_high", np.percentile(m_total, 95))

lognl = h['samples'].attrs['lognl']
logL = np.max(h['samples']['loglikelihood'][:])
print("SNR_maxL", snr_from_loglr(logL-lognl))

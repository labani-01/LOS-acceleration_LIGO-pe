
# Generated different LOS acceleration probability density plots using the following code

import numpy as np
import matplotlib.pyplot as pp
import pycbc.waveform
import h5py
from scipy.stats import gaussian_kde

plt.rcParams.update({
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 18
})

files = [
    "file1.hdf",
    "file2.hdf"
]
labels = ["1", "2"]
colors = ["color1", "color2"]


fig, ax = plt.subplots(figsize=(8, 6))

for file_path, label, color in zip(files, labels, colors):
    with h5py.File(file_path, "r") as f:
        data = f["samples/acc"][:]

        iqr = np.percentile(data, 75) - np.percentile(data, 25)

        a_5 = np.percentile(data, 5)
        a_50 = np.percentile(data, 50)
        a_95 = np.percentile(data, 95)
        lower_err = a_50 - a_5
        upper_err = a_95 - a_50
        print(f"{label}:", a_50, -lower_err, +upper_err)

        data_min, data_max = np.min(data), np.max(data)
        padding = (data_max - data_min) * 0.1
        x = np.linspace(data_min - padding, data_max + padding, 1000)

        bw_factor = 0.3
        kde = gaussian_kde(data, bw_method=bw_factor)
        y = kde(x)

        y0 = kde(0)
        print("posterior_zero_acc = ", y0)

        label_text = (
            f"{label} "):

        ax.plot(x, y, color=color, label=label_text)
        ax.axvline(a_5,  color=color, linestyle="--", alpha=0.5)
        ax.axvline(a_95, color=color, linestyle="--", alpha=0.5)
        ax.legend(fontsize=18, bbox_to_anchor=(0.4, 0.85), loc='best')

plt.xlabel(r"LOS acceleration ($\mathrm{cs}^{-1}$)")
plt.yticks([])
plt.legend(fontsize=13)
plt.xlim(-0.0075, 0.005)
plt.tight_layout()
plt.savefig("LOS_acc_prob_density.png")
plt.show()

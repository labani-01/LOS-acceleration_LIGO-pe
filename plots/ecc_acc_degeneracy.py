import numpy as np
import matplotlib.pyplot as pp
import h5py
from pycbc.filter.matchedfilter import overlap
from pycbc.conversions import snr_from_loglr
import corner

plt.rcParams.update({
    "axes.labelsize": 14,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "axes.titlesize": 13,
})

f = h5py.File("combined_acc_ecc_samples_pycbc_format_0p355_extracted_thinned_git.hdf", "r")

acc_samples = f['samples']['acc'][:]
ecc_samples = f['samples']['eccentricity'][:]

samples = np.column_stack([acc_samples, ecc_samples])

fig = corner.corner(
    samples,
    labels=[
        r"LOS acceleration ($c\,\mathrm{s}^{-1}$)",
        r"Eccentricity",
    ],
    show_titles=False,
    plot_datapoints=False,
    quantiles=[0.05, 0.5, 0.95],
    plot_contours=False,
    plot_density=False,
    figsize=(14, 11),
    label_kwargs={"fontsize": 14},
)


axes = np.array(fig.axes).reshape((2, 2))
ax2d = axes[1, 0]

# LOS-acceleration result
acc_scaled = acc_samples * 1e4
q5, q50, q95 = np.percentile(acc_scaled, [5, 50, 95])

err_plus = q95 - q50
err_minus = q50 - q5

axes[0, 0].set_title(
    "LOS acceleration\n"
    rf"$= {q50:.2f}^{{+{err_plus:.2f}}}_{{-{err_minus:.2f}}}"
    rf"\times 10^{{-4}}\ c\,\mathrm{{s}}^{{-1}}$",
    fontsize=12,
    pad=10,
)

# Eccentricity result
eq5, eq50, eq95 = np.percentile(ecc_samples, [5, 50, 95])

e_plus = eq95 - eq50
e_minus = eq50 - eq5

axes[1, 1].set_title(
    "Eccentricity\n"
    rf"$= {eq50:.3f}^{{+{e_plus:.3f}}}_{{-{e_minus:.3f}}}$",
    fontsize=12,
    pad=10,
)

# SNR-colored samples
logL = f["samples"]["loglikelihood"][:]
lognl = f["samples"].attrs["lognl"]
snr = snr_from_loglr(logL - lognl)

sc = ax2d.scatter(
    acc_samples,
    ecc_samples,
    c=snr,
    s=3,
    cmap="plasma",
    alpha=0.99,
)


fig.subplots_adjust(
    left=0.12,
    bottom=0.13,
    right=0.84,
    top=0.91,
    wspace=0.05,
    hspace=0.05,
)

cax = fig.add_axes([0.87, 0.14, 0.022, 0.76])
cbar = fig.colorbar(sc, cax=cax)
cbar.set_label("Network SNR", fontsize=14)
cbar.ax.tick_params(labelsize=13)

plt.show()

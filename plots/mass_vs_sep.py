import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 18
})

G = 6.67430e-11
c = 2.99792458e8
Msun = 1.98847e30

a_max = 0.0015*c

x = np.logspace(1, 4, 1000)

gamma_list = [0, 30, 60, 80]

M_min_plot = 10
M_max_plot = 1e6

plt.figure(figsize=(8,6))

for gdeg in gamma_list:
    g = np.radians(gdeg)
    cosg = np.maximum(np.cos(g), 1e-6)

    M_min_curve = (c**4 * cosg) / (4 * G * a_max * x**2)
    M_min_curve_sun = M_min_curve / Msun

    plt.plot(x, M_min_curve_sun, label=f'γ={gdeg}°')

    plt.fill_between(
        x,
        0,
        M_min_curve_sun,
        alpha=0.25
    )

plt.xscale('log')
plt.yscale('log')

plt.xlabel(r'$R [R_{\rm sch}]$')
plt.ylabel(r'M [$M_\odot$]')

plt.text(
    2e1,
    2e5,
    r'Allowed region: $a_{\rm obs} <= 0.0015c/sec$',
    fontsize=14
)

plt.ylim(M_min_plot, M_max_plot)
plt.xlim(1e1, 1e4)
plt.grid(True, which='both', alpha=0.2)
plt.legend()

plt.tight_layout()
plt.savefig("M_vs_R_plot.png")
plt.show()

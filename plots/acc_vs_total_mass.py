import numpy as np
import matplotlib.pyplot as pp
import h5py

data_GWTC4 = [ #mag_acc, total mass, totalmass-err, totalmass+err, snr
     (0.0271894544226212, 71.0381748563074, 69.3780579892409, 72.1643587096003, 78.4942695290203), #GW250114
     (0.000135706006923971, 9.72247269714284, 7.66288434171425, 12.1061244675258, 13.80585349483822), #GW230518
     (6.4844726797509E-05, 5.06261580405635, 4.67231522752379, 6.17828223850052, 12.096067291558946), #GW230529
     (0.0929960944380091, 66.0664566710341, 63.2738898097564, 69.3262777704137, 43.51282322251388), #GW230814_230901
     (0.02745617495691, 22.8499171970075, 21.470996379698, 26.1990100152068, 10.43555112735491), #GW231113_200417
     (0.000498725215282825, 15.1778017098331, 14.7111432081067, 16.6006950354397, 28.893948625185732), #GW230627_015337
     (0.0652387750834627, 26.0408485909386, 24.1660627086501, 33.4484358190067, 9.310334016915675), #GW230729_082317
     (0.0373405717339388, 47.4091903226907, 45.2387744351467, 49.5978306739967, 19.724505697839447), #GW230927_153832
     (0.0617064140415663, 34.3864493144896, 32.1114480308699, 38.7413059908958, 11.234481146169063), #GW230605_065343
     (0.0143485236116048, 20.2729243761741, 19.3029051281617, 22.6040858268644, 9.87103850089199), #GW230630_234532
     (0.00696446402099671, 24.0967996907414, 22.6170378948674, 31.1531163353423, 11.844072810149965), #GW231020_142947
     (0.00998389322951221, 26.7232557374767, 25.7939928712662, 29.2124171607704, 11.164688893604023), #GW231104_133418
     (0.0190971366943267, 22.4677959580338, 21.7061268647768, 26.0166394039381, 9.985082352187357), #GW231223_075055
     (0.0319039397350777, 23.0767640480105, 21.942252552854, 25.1226761686858, 10.99165084613942), #GW231223_202619
     (0.00819777063804261, 19.650422189011, 19.0998460893426, 20.7232135988233, 13.95779016177999), #GW231224_024321
     (0.0016741856454274505, 20.52278168062806, 20.081855822229798, 22.128385522870747, 21.92410403204945), #GW241102_124058
     (0.010915716337875, 25.3714969930357, 24.2167313193885, 33.3930995657195, 10.856384221497256), #GW231118_090602
     (0.00161555592897056, 26.2652420841328, 24.3628275919445, 29.4043449531504, 36.99943607071978), #GW241011_233834
     (0.00311882757721305, 23.0144299820547, 22.7281966802972, 23.6296708368912, 20.78876087304284) #GW250119_190238
]

data_GWTC123 = [
      (9.184751357719286e-06, 3.4254496080193872, 3.4151910733146678, 3.4794237669538193, 12.764838002119143), #GW190425
      (0.000895450640608794, 8.18007921257759, 6.18241977600742, 11.007204295689, 10.851919848979206), #GW200115
      (0.0026270881690716678, 27.472128361725595, 24.956559943447367, 29.213593962476825, 25.202603222892073), #GW190814
      (0.00661963105643526, 23.441199064812956, 22.13452026432365, 28.154836525182834, 13.26696569067995), #GW151226_033853
      (0.00951131499059665, 23.1250352353682, 22.4339306254167, 24.8347436433873, 13.134232891191475) , #GW190707_093326
      (0.00175115987869493, 10.5878969539954, 8.36752376295441, 15.623804650203, 14.382109792182918), #GW200105
      (2.12802632088005e-06, 2.757986389237105, 2.751548528069604, 2.7943145775600695, 35.12820853213628), #GW170817
      (0.0104454272694956, 19.7692068657248, 19.1794107406195, 22.6819759592374, 15.264720696217912), #GW170608
      (0.0411761716739186, 25.60074048271, 23.5475518643384, 31.3186862489551, 10.644366319192304), #GW190720_000836
      (0.0258004575275285, 19.0772420625614, 18.3263971814722, 21.6232828002029, 10.748883451720113), #GW200202_154313
      (0.064535386959576, 23.7013993154133, 21.8143718201075, 28.5119691453067, 13.5679428240641), #GW190728_064510
      (0.00185013283096014, 15.4289432317578, 14.6625521625189, 18.2418567801687, 12.532612447981347), #GW190924_02184
      (0.0541486646505085, 23.5194549281691, 21.7363744287415, 35.6290560809555, 9.956441240233882), #GW190930_133541
      (0.0406074897518203, 26.0557934465414, 24.4246970759495, 31.4170282313266, 8.73447303043076), #GW191126_115259
      (0.0133225663223545, 20.6076550846946, 19.26757160337, 24.0154601189762, 12.99453158000468), #GW191129_134029
      (0.011037265791860939, 23.044482720611736, 22.032582333931344, 26.2435739982401, 17.729084100651946), #GW191204_171526
      (0.014207157258740777, 21.217819189626304, 20.26090317876755, 24.616687734426403, 18.381421980287687), #GW191216_213338
      (0.01975671013858088, 26.05297175932629, 24.0110070667003, 39.686568422178766, 9.864700777252045), #GW200316_215756
       ]


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import matplotlib.colors as mcolors

plt.rcParams.update({
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'axes.labelsize': 20,
    'legend.fontsize': 20
})


# STRETCHED LOG SCALE FUNCTIONS

thresh = np.log10(1)
stretch = 2

def forward(y):
    y = np.asarray(y, dtype=float)
    result = np.full_like(y, np.nan)
    mask = y > 0
    log_y = np.zeros_like(y)
    log_y[mask] = np.log10(y[mask])
    below = mask & (log_y <= thresh)
    above = mask & (log_y > thresh)
    result[below] = log_y[below]
    result[above] = thresh + stretch * (log_y[above] - thresh)
    return result

def inverse(t):
    t = np.asarray(t, dtype=float)
    below = t <= thresh
    above = t > thresh
    log_y = np.zeros_like(t)
    log_y[below] = t[below]
    log_y[above] = thresh + (t[above] - thresh) / stretch
    return 10 ** log_y

# PREPARE DATA

def prepare_data(data):
    M_total = []
    acc = []
    snr = []
    M_lower = []
    M_upper = []

    for entry in data:
        acc_val = float(entry[0])
        mass = float(entry[1])

        err_low = float(min(entry[2], entry[3]))
        err_high = float(max(entry[2], entry[3]))

        M_total.append(mass)
        acc.append(acc_val)
        snr.append(float(entry[4]))
        M_lower.append(err_low)
        M_upper.append(err_high)

    return (np.array(M_total),
            np.array(acc),
            np.array(snr),
            np.array(M_upper),
            np.array(M_lower))

M1, acc1, snr1, M1_up_err, M1_low_err = prepare_data(data_GWTC123)
M2, acc2, snr2, M2_up_err, M2_low_err = prepare_data(data_GWTC4)


yerr1 = np.zeros((2, len(acc1)))
yerr2 = np.zeros((2, len(acc2)))

# COLORMAP

cmap = plt.get_cmap("turbo")
all_snr = np.concatenate([snr1, snr2])
norm = mcolors.LogNorm(vmin=min(all_snr), vmax=max(all_snr))

# CREATE FIGURE

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(16, 12), sharex=True,
    gridspec_kw={'height_ratios': [4, 2], 'hspace': 0.08}
)

# PLOT DATA

for ax in [ax1, ax2]:

    # --- GWTC 1/2/3 ---
    sc1 = ax.scatter(M1, acc1, c=snr1, cmap=cmap, norm=norm,
                     s=90, marker="v", edgecolor='k', zorder=4)

    # GWTC 1/2/3
    for i in range(len(M1)):
        color = cmap(norm(snr1[i]))
    
        ax.plot([M1_low_err[i], M1_up_err[i]],
                [acc1[i], acc1[i]],
                linestyle='--', color=color, linewidth=1, zorder=3)

    # --- GWTC 4 ---
    sc2 = ax.scatter(M2, acc2, c=snr2, cmap=cmap, norm=norm,
                     s=90, marker="v", edgecolor='k', zorder=4)

        # GWTC 4
    for i in range(len(M2)):
        color = cmap(norm(snr2[i]))
    
        ax.plot([M2_low_err[i], M2_up_err[i]],
                [acc2[i], acc2[i]],
                linestyle='--', color=color, linewidth=1, zorder=3)

    # --- Simulation point ---
    ax.scatter(30, 1e-11, c='red', s=150,
               marker='o', edgecolor='k', zorder=5)

    ax.set_xscale('log')

# APPLY Y-SCALES

ax1.set_yscale('function', functions=(forward, inverse))
ax2.set_yscale('log')

ax1.set_ylim(1e-7, 1)
ax2.set_ylim(1e-15, 1e-10)

# FIXED UPPER Y-TICKS (10^-1 to 10^-4)

upper_ticks = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]

ax1.set_yticks(upper_ticks)
ax1.set_yticklabels([
    r'$10^{-6}$',
    r'$10^{-5}$',
    r'$10^{-4}$',
    r'$10^{-3}$',
    r'$10^{-2}$',
    r'$10^{-1}$'
])

# Turn off minor ticks on stretched scale
ax1.yaxis.set_minor_locator(mticker.NullLocator())


# BROKEN AXIS

ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(bottom=False)

d = 0.015
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), **kwargs)
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)

kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

# LABELS & COLORBAR
ax2.set_xlabel("Total detector frame mass ($M_\\odot$)")
ax1.set_ylabel("Upper bound on |acc| ($\\mathrm{cs}^{-1}$)")

cbar = fig.colorbar(sc1, ax=[ax1, ax2], pad=0.02)
cbar.set_label("SNR", rotation=90, labelpad=18)

ax2.hlines(1e-14, 10, 300, colors='black', linestyles='--', linewidth=1.5, label='optimistic value of acceleration through LISA for 1 cycle dephasing')


ax1.annotate(
    "GW230814",
    xy=(65, 0.04),   # point location
    xytext=(10, 10), # offset in points
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW230529",
    xy=(9.7, 4e-5),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW200115",
    xy=(3.2, 4e-4),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW230518",
    xy=(5, 2e-5),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)


ax1.annotate(
    "GW190425",
    xy=(3.42, 0.000003),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW190814",
    xy=(28, 14e-4),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)


ax1.annotate(
    "GW200105",
    xy=(4, 0.0011),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)


ax2.annotate(
    "AGN Simulation based \n Keplerian acceleration",
    xy=(7, 0.9e-11),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=16,
    color='black',
    zorder=10
)

ax2.annotate(
"Optimistic LOS acceleration with LISA",
    xy=(10, 0.2e-13),
    xytext=(10, 10),
    textcoords='offset points',
   fontsize=16,
    color='black',
   zorder=10
)

ax1.annotate(
    "GW170817",
    xy=(2.8, 1e-6),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW250114",
    xy=(70, 0.008),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)

ax1.annotate(
    "GW241011",
    xy=(25, 6e-4),
    xytext=(10, 10),
    textcoords='offset points',
    fontsize=14,
    color='black',
    ha='left',
    va='bottom',
    zorder=10
)



# X AXIS

ax2.set_xticks([1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300])
ax2.xaxis.set_major_formatter(mticker.ScalarFormatter())
ax2.ticklabel_format(axis='x', style='plain')
ax1.set_xlim(1, 150)
ax2.set_xlim(1, 150)

plt.savefig("acc_vs_total_mass_step3.png",
           dpi=150, bbox_inches='tight')
plt.show()

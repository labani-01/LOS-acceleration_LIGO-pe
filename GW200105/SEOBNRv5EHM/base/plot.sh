pycbc_inference_plot_posterior --input-file ./result_2.hdf.bkup \
--output-file /home/lroy02/acceleration_runs/GW200105_runs/base/gw200105_ecc_acc.png \
--parameters inclination mchirp q spin1z spin2z eccentricity anomaly \
             'mass1_from_mchirp_q(mchirp, q):mass1' \
             'mass2_from_mchirp_q(mchirp, q):mass2' \
             acc \
--z-arg snr \

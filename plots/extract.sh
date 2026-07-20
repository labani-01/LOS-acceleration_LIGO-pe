pycbc_inference_extract_samples --verbose\
    --input-file posterior.hdf \
    --output-file posterior_extract.hdf \
    --parameters \
              mchirp q \
              loglikelihood \
              'mass1_from_mchirp_q(mchirp, q):mass1' \
              'mass2_from_mchirp_q(mchirp, q):mass2' \
             "mass1_from_mchirp_q(mchirp, q)+mass2_from_mchirp_q(mchirp, q):M_total" \
             "abs(acc):acc_mag" \
             acc \
    --force

#!/bin/bash

/home/lroy02/miniconda3/envs/ground_acc_env_6_BNS/bin/pycbc_inference \
--config-file /home/lroy02/ground_based_acc/separate_runs/GW170817/config_nonzero_a_IMRPhenomPv2_NRTidal.ini \
--nprocesses 64 \
--processing-scheme mkl \
--output-file /home/lroy02/ground_based_acc/separate_runs/GW170817/inference_nonzero_a_IMRPhenomPv2_NRTidal.hdf \
--seed 190814 \
--force \
--verbose

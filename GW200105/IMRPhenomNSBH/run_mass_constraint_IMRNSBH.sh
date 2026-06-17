#!/bin/bash
#SBATCH --job-name=pycbc_mpi
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --mem=256G
#SBATCH --time=14-00:00:00
#SBATCH --output=inference_mass_constraint_IMRNSBH3.out
#SBATCH --exclude=node[1110,1157]
#SBATCH --partition=compute_zone2,gpu_zone2

# Clean any pre-loaded modules to avoid conflicts
module purge

# ------------------ Safe Temporary Paths Setup ------------------

# Use SLURM's node-local tmp dir if available, fallback to /tmp
export TMPDIR="${SLURM_TMPDIR:-/tmp}/tmp_$SLURM_JOB_ID"
mkdir -p "$TMPDIR"

# Direct temporary and cache files to local space (avoid NFS issues)
export MPLCONFIGDIR="$TMPDIR/mpl"
export PYTHONPYCACHEPREFIX="$TMPDIR/pycache"
export NUMBA_CACHE_DIR="$TMPDIR/numba_cache"
export NUMBA_DISABLE_CACHE=1
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1

# OpenMPI settings for TCP communication
export OMPI_MCA_pml=ob1
export OMPI_MCA_btl=self,tcp
export OMPI_MCA_btl_tcp_if_include=10.59.0.0/16

# Debug print
echo "Host: $(hostname)"
echo "TMPDIR=$TMPDIR"
echo "NUMBA_DISABLE_CACHE=$NUMBA_DISABLE_CACHE"

# ------------------ Conda Environment Setup ------------------

# Initialize Conda
eval "$(/home/lroy02/miniconda3/bin/conda shell.bash hook)"
conda activate acc_SEOBNR-ecc_constraint


# ------------------ Launch PyCBC Inference ------------------

mpirun -np $SLURM_NTASKS -- pycbc_inference \
	--config-file /home/lroy02/acceleration_runs/separate_runs/GW200105/config_nonzero_a_mass_constraint_IMRNSBH2.ini \
	--output-file /home/lroy02/acceleration_runs/separate_runs/GW200105/inference_nonzero_a_mass_constraint_IMRNSBH3.hdf \
	--verbose --use-mpi


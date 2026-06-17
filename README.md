# Constraints on Line-of-Sight Acceleration from O1–O4a

**Labani Roy¹ and Alexander H. Nitz¹**  
¹ Department of Physics, Syracuse University, Syracuse, NY 13244, USA  

---

## Overview

This repository contains the data and code associated with the study:

> *Constraints on Line-of-Sight Acceleration from O1–O4a*

The project measures line-of-sight (LOS) acceleration using all available gravitational-wave observations from the first four observing runs (O1–O4a) of LIGO and Virgo.

We introduce a new method to model the LOS acceleration by directly applying the time-varying Doppler in the time domain to the signal produced in the binary's frame; this method can be applied to any waveform model including those with higher order modes, eccentricity, and precession.

Across all analyzed events, we find results consistent with zero LOS acceleration.

---

## Installation

For installing the waveform model, please follow these steps:

### 1. Create environment

```bash
conda create -n acc_env python=3.11
conda activate acc_env
```

### Install PyCBC

```bash
mkdir LOS_acc
cd LOS_acc
git clone git@github.com:gwastro/pycbc.git
cd pycbc
pip install -r requirements.txt
pip install -r companion.txt
pip install .
cd ..
``` 

### Install acceleration waveform

```bash
git clone git@github.com:labani-01/pycbc_acceleration_waveform.git
cd pycbc_acceleration_waveform
pip install .
cd ..
```


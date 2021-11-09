import os
import sys
import moments
import matplotlib
matplotlib.use('pdf')
import pylab
import matplotlib.pyplot as plt
import numpy as np
#from numpy import array
# from moments import Misc,Spectrum,Numerics,Manips,Integration,Demographics1D,Demographics2D
from datetime import datetime
import Models_2D

# infile="../easySFS/output_linked_noOut_100_100_100_100/dadi/pure1_adult-pure2_adult.sfs"
infile="../easySFS/output_linked_noOut_100_100_100_100/dadi/pure2_juv-pure1_juv.sfs"
# infile="../easySFS/output_linked_noOut_50_50/dadi/pure1-pure2.sfs"
# infile=sys.argv[1]
# pop_ids=[sys.argv[2],sys.argv[3]]
# projections=[int(sys.argv[4]),int(sys.argv[5])]
model_best=Models_2D.sym_mig_size
# model_best=sys.argv[6] #name of best model, ie Models_2D.InsertNameOfModel
#outfile=sys.argv[6]

fs = moments.Spectrum.from_file(infile)
ns = fs.sample_sizes
pop_ids = fs.pop_ids

# np.set_printoptions(precision=3)


# enter ml params of best model
# params_ml = [3.025,4.0956,25.4131,28.4665,9.8444,1.1646,0.6569] #ad 
params_ml = [2.0337,3.9423,29.8496,29.536,11.4636,2.5506,0.9433] #juv
# param_labels = "nu1, nuA, nu2, nu3, m1, m2, T1, T2, T3"

#simulate the best model with the ml parameters to make sfs
sim_model = model_best(params_ml, fs.sample_sizes)

# Optimially scale model sfs to data sfs
fs_model = moments.Inference.optimally_scaled_sfs(sim_model, fs)

# fold modeled sfs
sim_model = sim_model.fold()
fs_model = fs_model.fold()

# Heatmap of single 2d SFS
moments.Plotting.plot_single_2d_sfs(fs, show=False, out="sfs_observed.png")
moments.Plotting.plot_single_2d_sfs(sim_model, show=False, out="sfs_model.png")
moments.Plotting.plot_single_2d_sfs(fs_model, show=False, out="sfs_model_scaled.png")

# Poisson comparison between 2d model and data.
# moments.Plotting.plot_2d_comp_Poisson(fs_model, fs, out="sfs_comp_pois_scaled.png")
moments.Plotting.plot_2d_comp_Poisson(sim_model, fs, resid_range=1000, out="sfs_comp_pois.png")

# Multinomial comparison between 2d model and data.
# moments.Plotting.plot_2d_comp_multinom(fs_model, fs)
# moments.Plotting.plot_2d_comp_multinom(sim_model, fs, out="sfs_comp_multinom.png")

# Linear heatmap of 2d residual array.
# resid_pois = moments.Inference.linear_Poisson_residual(fs_model, fs, mask=None)
# resid_ansc = moments.Inference.Anscombe_Poisson_residual(fs_model, fs, mask=None)
# moments.Plotting.plot_2d_resid(resid_pois)
# moments.Plotting.plot_2d_resid(resid_ansc)

# resid_pois = moments.Inference.linear_Poisson_residual(sim_model, fs, mask=None)
# resid_ansc = moments.Inference.Anscombe_Poisson_residual(sim_model, fs, mask=None)
# moments.Plotting.plot_2d_resid(resid_pois, out="sfs_resid_pois.png")
# moments.Plotting.plot_2d_resid(resid_ansc, out="sfs_resid_ansc.png")

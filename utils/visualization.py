import matplotlib.pyplot as plt
import numpy as np
import os

PLOT_DIRS = 'stuff/results/plots/histograms'

if not os.path.exists(PLOT_DIRS):
  os.makedirs(PLOT_DIRS)

#@title Function: Plot Histograms
def plot_histograms(dict_arrays = None, bins = 10, title="", filename = None, save_name = "default_hist.svg", save = False):
  

  #Verification for load dict of arrays
  if dict_arrays is None:
    if filename:
      print("[Load] proximities data: ",filename)
      dict_arrays = np.load(filename)
    else:
      print("[Error] define a dict of arrays or load from a .npz file")

 

  inches = 4
  cols = 4
  rows =  int(len(dict_arrays) / cols)

  fig, ax = plt.subplots(rows,cols, figsize = (inches*cols,inches*rows))

  i = 0
  j = 0
  for k, arr in dict_arrays.items():

    ax[i,j].hist(arr, bins=bins)
    ax[i,j].set_title("{}{}".format(title, k))
    j += 1
    if j == cols: 
      i += 1
      j = 0

  if save:
    plt.savefig(os.path.join(PLOT_DIRS,save_name))
    
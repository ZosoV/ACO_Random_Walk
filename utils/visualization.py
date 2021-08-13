import matplotlib.pyplot as plt
import numpy as np
import os
from utils.measures import get_pheromones_per_node

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
  rows =  int(np.ceil(len(dict_arrays) / cols))

  fig, ax = plt.subplots(rows,cols, figsize = (inches*cols,inches*rows))
  
  if rows != 1:
    i = 0
    j = 0
    for k, arr in dict_arrays.items():

      ax[i,j].hist(arr, bins=bins)
      ax[i,j].set_title("{}{}".format(title, k))
      j += 1
      if j == cols: 
        i += 1
        j = 0
  else:
    i = 0
    for k, arr in dict_arrays.items():

      ax[i].hist(arr, bins=bins)
      ax[i].set_title("{}{}".format(title, k))
      i += 1

  if save:
    plt.savefig(os.path.join(PLOT_DIRS,save_name))
    
#@title Function to plot the graph in a grid prespective, the pheromones and exploration
def draw_progress(base_class, iter, ant, step, draw_additional = False):
  # Create a canvas to display the visited cells, the ant, and the target
  # values: to traget, free cells, and obstacles
  canvas = [ base_class.graph.nodes[i]['state'].value for i in sorted(base_class.graph.nodes()) ]
  # values: to the visited cells
  for node in base_class.visited_nodes: canvas[node] = 0.2
  # values: to the ant
  canvas[base_class.current_position] = 0.3

  canvas = np.array(canvas).reshape((base_class.size, base_class.size))

  def draw_grid_inner(ax):
      ax.set_title('Iteration {} - Ant {} - Step {}'.format(iter,ant,step))
      ax.pcolor(canvas, edgecolors='k', cmap='Paired', linewidths=0.2, vmin = 0., vmax = 1.0)
      ax.set_aspect('equal') #set the x and y axes to the same scale
      plt.xticks(np.arange(0.5, base_class.size, step=1), labels=[i for i in range(base_class.size)]) 
      plt.yticks(np.arange(base_class.size - 0.5, 0, step=-1), labels=[i for i in range(base_class.size)])
      ax.invert_yaxis() #invert the y-axis so the first row of data is at the top
  
  def pheromones_plot(fig, ax):
      pheromones = get_pheromones_per_node(base_class.graph)
      im = ax.pcolor(pheromones, edgecolors='k', cmap='viridis', linewidths=0.2)
      ax.set_title('Pheromones Distribution')
      ax.set_aspect('equal') #set the x and y axes to the same scale
      ax.set_xticks([])
      ax.set_yticks([])
      ax.invert_yaxis() #invert the y-axis so the first row of data is at the top
      
      cbar=fig.colorbar(im, label='pheromones amount', ax = ax)
    
  def exploration_plot(fig, ax):
      exploration = [ base_class.graph.nodes[i]['counter'] for i in sorted(base_class.graph.nodes()) ]
      exploration = np.array(exploration).reshape((base_class.size, base_class.size))
      im2 = ax.pcolor(exploration, edgecolors='k', cmap='plasma', linewidths=0.2)
      ax.set_title('Exploration')
      ax.set_aspect('equal') #set the x and y axes to the same scale
      ax.set_xticks([])
      ax.set_yticks([])
      ax.invert_yaxis() #invert the y-axis so the first row of data is at the top
      
      cbar=fig.colorbar(im2, label='number of times visited', ax = ax)
    
  fig, ax = plt.subplots( figsize=(3*base_class.size/4,2*base_class.size/4))

  ax1 = plt.subplot(231)
  ax2 = plt.subplot(232)
  ax3 = plt.subplot(233)

  #ax4 = plt.subplot(212)

  #Plot the maze
  if draw_additional:

      draw_grid_inner(ax1)
        
      pheromones_plot(fig,ax2)
    
      exploration_plot(fig,ax3)
     
      #list_iterations = np.arange(0, len(base_class.list_distances))
      #ax4.plot(list_iterations, base_class.list_distances, "b-") #, label = label)
    
  else:
      draw_grid_inner(ax1)
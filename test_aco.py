# script for testing aco without random walks
import os

from networkx.classes import graph
from model.graph_env import PPGraph
from model.aco import ACOPP
import random_walk.rw_models as rw
import numpy as np

# directories
EXPERIMENT_NAME = "evaporation_rate"
SAVING_DIR = "stuff/results/aco_pp/histories_{}/".format(EXPERIMENT_NAME)
SIZE = 20

if not os.path.exists(SAVING_DIR):
    os.makedirs(SAVING_DIR)

# Define the parameters of our model
ants = 10
tau_0 = 1
alpha = 3. 
beta = 2.
p = 0.3
intensity = None
local_p = 0
q_0 = 0.3

# Additional attributes
penalty = 0.7 # Nota el grado de penalización provoca que haya mas o menos ruido

total_iter = 500
iter_show = 50

# Create the graph
graph = PPGraph(size = SIZE, tau_0 = tau_0)

# Create the optimizer using the current graph
optimizer = ACOPP(graph, ants, alpha, beta, p, penalty, local_p, intensity, q_0)

# Execute the optimizer
history = optimizer.fit(total_iter,iter_show = iter_show)

file_name = "history_{}_{}_{}_{}_{}_{}_{}.npy".format(
    ants,
    alpha,
    beta,
    p,
    q_0,
    penalty,
    total_iter)

file_dir = os.path.join(SAVING_DIR,file_name)

np.save(file_dir, history)
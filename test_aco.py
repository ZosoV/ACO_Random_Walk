# script for testing aco without random walks
import os

from networkx.classes import graph
from model.graph_env import PPGraph
from model.aco import ACOPP
import random_walk.rw_models as rw
import numpy as np
import pandas as pd
import argparse
import sys
import logging
logging.basicConfig(format='%(asctime)s | line: %(lineno)d | %(levelname)s: %(message)s', level=logging.NOTSET)

parser = argparse.ArgumentParser(description='Test Ant Colony System algorithm')
parser.add_argument('--exp_name', default=None, type=str,
                    help='the name of the experiment that you want to execute', required=True)
parser.add_argument('--exp_file', default="stuff/experiments/params_experiments.xlsx", type=str,
                    help='the file where is stored the specifications of your experiment')
args = parser.parse_args()

# File with the experiments specifications
SEED = 10000
EXPERIMENT_FILE = args.exp_file
TOTAL_ITER = 200
ITER_SHOW = 25
EXECUTIONS_PER_EXPERIMENT = 3

# Init to a particular seed
np.random.seed(SEED)

# Opening xlsx file with the parameters specifications
params = pd.read_excel(EXPERIMENT_FILE, sheet_name=args.exp_name)

# Create a dir where I save the results
saving_dir = "stuff/results/aco_pp/histories_{}/".format(args.exp_name)     
if not os.path.exists(saving_dir):         
    os.makedirs(saving_dir)
    
# 
logging.info("Running experiment: {}".format(args.exp_name))
logging.info("\n {}".format(params.head()))

for index, row in params.iterrows():
    for execution in range(EXECUTIONS_PER_EXPERIMENT):
        exp_info = "\n ------------------------------- \n"
        exp_info += f"| Running sub experiment: {index} execution: {execution} \n"
        exp_info += f'| size: {row["size"]} \n'
        exp_info += f'| ants: {row["ants"]} \n'
        exp_info += f'| tau_0: {row["tau_0"]} \n'
        exp_info += f'| alpha: {row["alpha"]} \n'
        exp_info += f'| beta: {row["beta"]} \n'
        exp_info += f'| p: {row["p"]} \n'
        exp_info += f'| intensity: {row["intensity"]} \n'
        exp_info += f'| local_p: {row["local_p"]} \n'
        exp_info += f'| q_0: {row["q_0"]} \n'
        exp_info += f'| penalty: {row["penalty"]} \n'
        exp_info += f'| proximity: {row["proximity"]} \n'
        exp_info += "-------------------------------"
        logging.info(exp_info)
        
        # Create the graph
        graph = PPGraph(size = row['size'], tau_0 = row['tau_0'])

        # Create the optimizer using the current graph
        optimizer = ACOPP(graph, 
                            row["ants"], 
                            row["alpha"], 
                            row["beta"], 
                            row["p"], 
                            row["penalty"], 
                            row["local_p"] if not np.isnan(row['local_p']) else None, 
                            row["intensity"] if not np.isnan(row['intensity']) else None, 
                            row["q_0"],
                            row['proximity'] )

        # Execute the optimizer
        history = optimizer.fit(TOTAL_ITER,iter_show = ITER_SHOW)

        file_name = "history_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_exc_{}.npy".format(
            row["size"],
            row["ants"], 
            row["tau_0"],
            row["alpha"], 
            row["beta"], 
            row["p"],
            row["intensity"],
            row["local_p"],
            row["q_0"],
            row["penalty"],
            row["proximity"],
            TOTAL_ITER,
            execution)

        file_dir = os.path.join(saving_dir,file_name)

        np.save(file_dir, history)
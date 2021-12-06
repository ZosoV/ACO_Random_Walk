# script for testing random walks
import os

from networkx.classes import graph
import model.graph_env as ge
import random_walk.rw_models as rw
import numpy as np
import pandas as pd

import argparse
from datetime import datetime
import logging

parser = argparse.ArgumentParser(description='Test Ant Colony System algorithm')
parser.add_argument('--exp_name', default=None, type=str,
                    help='the name of the experiment that you want to execute', required=True)
parser.add_argument('--exp_file', default="stuff/experiments/rw_experiments_1.xlsx", type=str,
                    help='the file where is stored the specifications of your experiment')
parser.add_argument('--exp_start', default=None, type=int,
                    help='the id of the experiment to start')
parser.add_argument('--exp_end', default=None, type=int,
                    help='the id of the experiment to end')
args = parser.parse_args()


date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

logging.basicConfig(
    filename=f"stuff/logs/{args.exp_name}_{date}.log",
    filemode='a',
    format='%(asctime)s | line: %(lineno)d | %(levelname)s: %(message)s', level=logging.NOTSET)

# File with the experiments specifications
SEED = 10000
EXPERIMENT_FILE = args.exp_file
TOTAL_ITER = 100
ITER_SHOW = 25

# Init to a particular seed
np.random.seed(SEED)

# Opening xlsx file with the parameters specifications
params = pd.read_excel(EXPERIMENT_FILE, sheet_name=args.exp_name)

# Create a dir where I save the results
saving_dir = "stuff/results/aco_pp/histories_{}/".format(args.exp_name)     
if not os.path.exists(saving_dir):         
    os.makedirs(saving_dir)


logging.info("Running experiment: {}".format(args.exp_name))
logging.info("\n {}".format(params.head()))

if args.exp_start is not None and args.exp_end is not None:
    params = params.loc[(params.index >= args.exp_start) & (params.index < args.exp_end)]

for index, row in params.iterrows():
    exp_info = "\n ------------------------------- \n"
    exp_info += f"| Running sub experiment: {index} \n"
    exp_info += f'| type: {row["type"]} \n'
    exp_info += f'| n_rw: {row["n_rw"]} \n'
    exp_info += f'| size: {row["size"]} \n'
    exp_info += f'| q_0: {row["q_0"]} \n'
    exp_info += "-------------------------------"
    logging.info(exp_info)

    # Create the graph
    graph = ge.PPGraph(size=row["size"], tau_0=0.1)

    # Create the walker
    if row["type"] == "greedy":
        walker = rw.GreedyWalker(graph, 
                            q_0 = row["q_0"], 
                            advantage = row["advantage"])
    elif row["type"] == "levy_greedy":
        walker = rw.LevyFlightGreedyWalker(graph, 
                                            q_0 = row["q_0"],
                                            omega = row["omega"],
                                            advantage = row["advantage"])
    elif row["type"] == "proximity":
        walker = rw.ProximityWalker(graph, 
                                q_0 = row["q_0"], 
                                proximity_mode = row["proximity"])

    elif row["type"] == "levy_proximity":
        walker = rw.LevyFlightProximityWalker(graph, 
                                q_0 = row["q_0"], 
                                omega = row["omega"],
                                proximity_mode = row["proximity"])
    else:
        logging.exception(f'The type {row["type"]} is not defined')

    # Perform the walk
    distances_list = walker.walk(row['n_rw'])


    file_name = "history_exp_{}.npy".format(
        str(index).zfill(2))
    file_dir = os.path.join(saving_dir,file_name)

    history = {
        "distances" : np.array(distances_list),
        "mean"  : np.mean(distances_list),
        "std"  : np.std(distances_list),
        "sem"  : np.std(distances_list, ddof=1) / np.sqrt(np.size(distances_list))
    }


    np.save(file_dir, history)
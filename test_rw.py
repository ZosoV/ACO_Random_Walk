# script for testing random walks
import os

from networkx.classes import graph
import model.graph_env as ge
import random_walk.rw_models as rw
import numpy as np

DATA_DIR = "stuff/data/random_maze/"
SAVING_DIR = "stuff/results/aco_pp/"
RANDOM_WALK_DIR = SAVING_DIR + "random_walks/"


def testing_levy_greedy(g_size, n_random_walks):
    type_rw = "levy_greedy"

    advantage_options = [2,2.5,3]
    q_0_options = [0, 0.3, 0.5, 0.7, 0.9]
    omega_options = [0.5, 1, 2, 3, 4]
    num_rand_walks = int(n_random_walks)

    # Create the graph
    graph = ge.PPGraph(size=g_size, tau_0=0.1)

    dir_results = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}")
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    dict2plot = {}

    for advantage in advantage_options:
        for q_0 in q_0_options:
            for omega in omega_options:

                # Create the walker
                walker = rw.LevyFlightGreedyWalker(graph, 
                                                q_0 = q_0,
                                                omega = omega,
                                                advantage = advantage)
                
                # Perform the walk
                distances_list = walker.walk(num_rand_walks)
                
                base_name = "advantage_{}_q0_{}_omega_{}".format(
                    advantage,
                    q_0,
                    omega)
                
                dict2plot[base_name] = np.array(distances_list)
                print("Saving ... {}.npy".format(base_name))

                file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}/{base_name}.npy")
                np.save(file_name, np.array(distances_list))

    file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}.npz")
    np.savez(file_name, **dict2plot) 

def testing_levy_proximity(g_size, n_random_walks):
    type_rw = "levy_proximity"
    proximities_options = ['proximity_1', 'proximity_2']
    distances_options = ['euclidean', 'manhattan']
    normalization_options = [ 'none', 'l2-norm', 'max-min']
    q_0_options = [0. , 0.3, 0.5, 0.7, 0.9]
    omega_options = [0.5, 1, 2, 3, 4]
    num_rand_walks = int(n_random_walks)

    # Create the graph
    graph = ge.PPGraph(size = g_size, tau_0 = 0.1)

    dir_results = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}")
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    dict2plot = {}
    for proximity in proximities_options:
        for distance in distances_options:
            for normalization in normalization_options:
                for q_0 in q_0_options:
                    for omega in omega_options:


                        # Create the walker
                        walker = rw.LevyFlightProximityWalker(graph, 
                                                q_0 = q_0, 
                                                reward_tau = 0.0001,
                                                omega = omega,
                                                proximity_mode = proximity,
                                                distance_type = distance,
                                                normalization = normalization)

                        # Perform the walk
                        distances_list = walker.walk(num_rand_walks = num_rand_walks)
                        
                        base_name = "{}_{}_{}_{}_omega_{}".format(
                            proximity,
                            distance,
                            normalization,
                            q_0,
                            omega)
                        
                        dict2plot[base_name] = np.array(distances_list)
                        print("Saving ... {}".format(base_name))
                        file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}/{base_name}.npy")
                        np.save(file_name, np.array(distances_list))

    file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}.npz")
    np.savez(file_name, **dict2plot)      

def testing_greedy(g_size, n_random_walks):
    type_rw = "greedy"

    advantage_options = [2,2.5,3]
    q_0_options = [0, 0.3, 0.5, 0.7, 0.9]
    num_rand_walks = int(n_random_walks)

    # Create the graph
    graph = ge.PPGraph(size=g_size, tau_0=0.1)

    dir_results = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}")
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    dict2plot = {}

    for advantage in advantage_options:
        for q_0 in q_0_options:


            # Create the walker
            walker = rw.GreedyWalker(graph, 
                                q_0 = q_0, 
                                advantage = advantage)
            
            # Perform the walk
            distances_list = walker.walk(num_rand_walks)
            
            base_name = "advantage_{}_q0_{}".format(
                advantage,
                q_0)
            
            dict2plot[base_name] = np.array(distances_list)
            print("Saving ... {}.npy".format(base_name))
            file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}/{base_name}.npy")
            np.save(file_name, np.array(distances_list))

    file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}.npz")
    np.savez(file_name, **dict2plot) 

def testing_proximity(g_size, n_random_walks):
    type_rw = "proximity"
    proximities_options = ['proximity_1', 'proximity_2']
    distances_options = ['euclidean', 'manhattan']
    normalization_options = [ 'none', 'l2-norm', 'max-min']
    q_0_options = [0. , 0.3, 0.5, 0.7, 0.9]

    num_rand_walks = int(n_random_walks)

    # Create the graph
    graph = ge.PPGraph(size = g_size, tau_0 = 0.1)

    dir_results = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}")
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    dict2plot = {}
    for proximity in proximities_options:
        for distance in distances_options:
            for normalization in normalization_options:
                for q_0 in q_0_options:


                    # Create the walker
                    walker = rw.ProximityWalker(graph, 
                                            q_0 = q_0, 
                                            reward_tau = 0.0001,
                                            proximity_mode = proximity,
                                            distance_type = distance,
                                            normalization = normalization)

                    # Perform the walk
                    distances_list = walker.walk(num_rand_walks = num_rand_walks)
                    
                    base_name = "{}_{}_{}_{}".format(
                        proximity,
                        distance,
                        normalization,
                        q_0)
                    
                    dict2plot[base_name] = np.array(distances_list)
                    print("Saving ... {}.npy".format(base_name))

                    file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}/{base_name}.npy")
                    np.save(file_name, np.array(distances_list))

    file_name = os.path.join(RANDOM_WALK_DIR,f"rw_{type_rw}_size_{graph.size}.npz")
    np.savez(file_name, **dict2plot)      

n_randwalk_options = [1e5, 1e5, 1e5, 1e5,  1e5, 1e4, 3500, 3500, 25]
graph_size_options = [ 10,  25,  50,  75,  100, 512, 1024, 2048, 4096] 

for idx, graph_size in enumerate(graph_size_options):
    testing_proximity(graph_size, n_randwalk_options[idx])
    # testing_greedy(graph_size, n_randwalk_options[idx])
    # testing_levy_proximity(graph_size, n_randwalk_options[idx])
    # testing_levy_greedy(graph_size, n_randwalk_options[idx])
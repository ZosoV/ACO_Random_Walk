
import numpy as np
from model.graph_env import State
from utils.measures import get_proximity
import logging

class AntColonyOptimizer():
  def __init__(self, graph, ants, alpha, beta, p, local_p = None, intensity = None, q_0 = None):
    """
    Ant colony optimizer.  Traverses a graph and finds the min weight distance
    :param graph: graph environment
    :param ants:  number of ants to traverse the graph
    :param alpha: weighting of pheromone
    :param beta:  weighting of heuristic
    :param p:     evaporation rate at which pheromone evaporates
    :param local_p: local evaporation rate at which pheromone evaporates (optional)
    :param intensity: the amount of pheromones to add per edge (optional)
    :param q_0: probability to choose the best construction step (optional)
    """
    self.graph = graph
    self.ants = ants
    self.alpha = alpha
    self.beta = beta
    self.p = p
    self.local_p = local_p
    self.intensity = intensity
    self.q_0 = q_0

    self.best_path = []
    self.reset_environment()


  def reset_environment(self):
    """ return to the base state of the environment
    """
    self.current_position = self.start_node
    self.visited_nodes = [self.start_node]
    self.current_path = []

  def is_visited(self, neighbor):
    """return if the neighbor has alreadey been visited
    """
    return neighbor in self.visited_nodes   
  
  def get_total_distance(self, path):
    """return the total distance of the given path
    """
    t_distance = 0
    for node1, node2 in path:
      t_distance += self.graph[node1][node2]['distance']

    # At the beginning, the total distance is define by inf
    if len(path) == 0 : t_distance = float('inf')
    return t_distance

  def update_best_path(self):
    if self.get_total_distance(self.current_path) < self.get_total_distance(self.best_path):
      self.best_path = self.current_path
  
  def local_evaporation(self, neighbor):
    edge = (self.current_position, neighbor)
    self.graph.edges[edge]['pheromone'] = (1 - self.local_p) * self.graph.edges[edge]['pheromone'] + self.local_p * self.graph.tau_0

  def offline_pheromone_update(self):
    """
    Here, it is performed two steps at the same time:

    1. global evaporation of the pheromone using self.p
    2. contribution of pheromones over the best path found so far. The 
    contribution or reward is defined according to the distance of the 
    best path found so far. Also, if intensity is defined you could 
    update using that constant vaue
    """
    cost = self.get_total_distance(self.best_path)
    reward = self.intensity if self.intensity is not None else 1 / cost

    #print("[INFO] Updating current path - cost: {} reward: {}".format(cost, reward))

    for node1, node2, _ in self.graph.edges(data=True):
      # 1. evaporation
      self.graph[node1][node2]['pheromone'] = (1 - self.p) * self.graph[node1][node2]['pheromone']

      # 2. contribution update
      if (node1, node2) in self.best_path or (node2, node1) in self.best_path:
        self.graph[node1][node2]['pheromone'] += self.p * reward

class ACOPP(AntColonyOptimizer):
  def __init__(self, graph, ants, alpha, beta, p, penalty, local_p = None, intensity = None, q_0 = None, proximity = 'prox1'):
    """
    Ant colony optimizer for Path Planning.  
    Traverses a graph and finds the min weight distance 
    between a start and target node
    
    :param graph: graph environment
    :param ants:  number of ants to traverse the graph
    :param alpha: weighting of pheromone
    :param beta:  weighting of heuristic
    :param p:     evaporation rate at which pheromone evaporates
    :param local_p: local evaporation rate at which pheromone evaporates (optional)
    :param penalty: penalization percent of already visited nodes 
    :param intensity: the amount of pheromones to add per edge (optional)
    :param q_0: probability to choose the best construction step (optional)
    :param proximity: choose what proximity measure use (optional)
    """    
    self.start_node = 0
    self.penalty = penalty
    self.size = graph.size
    self.target_node = self.size * self.size - 1
    self.list_distances = []
    self.proximity = proximity

    super().__init__(graph, ants, alpha, beta, p, local_p, intensity, q_0)

    self.graph.nodes[self.graph.size * self.graph.size - 1]['state'] = State.target

  def update_state(self, mode = 'proximity_1', 
                   normalization = None,
                   mean = 0, 
                   std = 1, 
                   distance = 'euclidean'):
    neighbors = self.graph[self.current_position]

    # Process to get the weight of each neighbor
    weights = []
    aux_weights = []
    neighbors_idx = []
    for neighbor_node, edge in neighbors.items():
      if self.graph.nodes[neighbor_node]['state'] != State.wall:
          proximity = get_proximity(self.graph, 
                                    self.current_position,
                                    neighbor_node,
                                    self.target_node,
                                    mode,
                                    distance)
          if normalization is not None:
            proximity = (proximity - mean) / std      

          if not self.is_visited(neighbor_node):
            # get the weight per neighbor and append it
            weights.append( (edge['pheromone'] ** self.alpha) * 
                          (proximity ** self.beta))
            aux_weights.append( edge['pheromone'] * 
                          (proximity ** self.beta))
            neighbors_idx.append(neighbor_node)
          else:
            penalty_pheromone = (1 - self.penalty) * edge['pheromone']
            weights.append( (penalty_pheromone ** self.alpha) * 
                  (proximity ** self.beta))
            aux_weights.append( penalty_pheromone * 
                          (proximity ** self.beta))
            neighbors_idx.append(neighbor_node)
    
    acu_weight = sum(weights)
    probabilities = np.array(weights)/acu_weight
    #print("[INFO] probabilities: {}".format(probabilities))

    # with probability q_0 select the best trial
    if self.q_0 is not None and np.random.rand() < self.q_0:
        new_position = neighbors_idx[np.argmax(aux_weights)]
    else:
      # choose an option following the wheel selection algorithm  
      new_position = np.random.choice(neighbors_idx, p=probabilities)

    # perform local evaporation
    if self.local_p is not None:
      self.local_evaporation(new_position)

    self.graph.nodes[self.current_position]['counter'] += 1
     
    self.current_path.append((self.current_position, new_position))
    self.visited_nodes.append(new_position)
    self.current_position = new_position

  def end_route(self):
    return self.current_position == self.target_node

  def fit(self, total_iter, steps_die = None, iter_show = 10):
    # define 2 draw_mode per_iteration or per_ants
    list_distances = []
    list_distances_avg = []
    list_distances_std = []
    list_distances_sem = []
    
    for iter in range(total_iter):

      distance_per_ants = []

      for ant in range(self.ants):
        get_target = False
        is_stuck = False
        step = 0
        while not get_target and not is_stuck:
          self.update_state(mode=self.proximity)     
          step += 1
            
          if steps_die == step: 
            is_stuck = True
          get_target = self.end_route()
          if get_target: self.graph.nodes[self.current_position]['counter'] += 1
          
        if not is_stuck: 
            self.update_best_path()
            is_stuck = False
        current_distance = self.get_total_distance(self.current_path)
        #print("[INFO] iter: {} ant: {} current: {}".format(iter, ant, current_distance))
        distance_per_ants.append(current_distance)
        self.reset_environment()

      self.offline_pheromone_update()

      # Track the best distance so far
      best_distance = self.get_total_distance(self.best_path)
      if iter % iter_show == 0:
        logging.info("iter: {} best: {:.2f} d_mean: {:.2f} d_stdv: {:.2f} d_sem: {:.2f}".format(iter, 
                                                              best_distance, 
                                                              np.mean(distance_per_ants),
                                                              np.std(distance_per_ants),
                                                              np.std(distance_per_ants, ddof=1) / np.sqrt(np.size(distance_per_ants))))
      list_distances.append(best_distance)
      list_distances_avg.append(np.mean(distance_per_ants))
      list_distances_std.append(np.std(distance_per_ants))
      list_distances_sem.append(np.std(distance_per_ants, ddof=1) / np.sqrt(np.size(distance_per_ants)))
      self.list_distances.append(best_distance)

    history = {
        "distances_best" : list_distances,
        "distances_avg"  : list_distances_avg,
        "distances_std"  : list_distances_std,
        "distances_sem"  : list_distances_sem
    }

    return history

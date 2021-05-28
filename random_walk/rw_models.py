from random_walk.walker import Walker
from utils.measures import get_proximity, normalize_array, get_distance
import numpy as np

class ProximityWalker(Walker):
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001,
               proximity_mode = 'proximity_1', distance_type = 'euclidean', 
               normalization = None):
    
    self.proximity_mode = proximity_mode
    self.distance_type = distance_type
    self.normalization = normalization
    super().__init__(graph, q_0, reward_tau)


  def update_step(self):
    neighbors = self.graph[self.current_position]

    weights = []
    neighbors_idx = []
    for neighbor_node, edge in neighbors.items():
        # get the weight per neighbor
        weights.append(get_proximity(self.graph, 
                                     self.current_position,
                                     neighbor_node, 
                                     self.target_node,
                                     self.proximity_mode,
                                     self.distance_type))
        neighbors_idx.append(neighbor_node)

    # applied local normalization
    if self.normalization is not None:
      weights = normalize_array(weights, self.normalization)
      

    if self.q_0 is not None and np.random.rand() < self.q_0:
      new_position = neighbors_idx[np.argmax(weights)]
  
    else:
      acu_weight = sum(weights)
      probabilities = np.array(weights)/acu_weight
      #print("[INFO] probabilities: {}".format(probabilities))

      # choose an option following the wheel selection algorithm  
      new_position = np.random.choice(neighbors_idx, p = probabilities)
      
    self.current_path.append((self.current_position, new_position))
    self.visited_nodes.append(new_position)
    self.current_position = new_position


class GreedyWalker(Walker):
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001, advantage = 3):

    self.advantage = advantage
    super().__init__(graph, q_0, reward_tau)

  def get_greedy_favorites(self, location = ('bottom','right') ):
    
    favorites_nodes = []
    if location[1] == 'right':
      favorites_nodes.append(self.current_position + 1)
    elif location[1] == 'left':
      favorites_nodes.append(self.current_position - 1)

    if location[0] == 'bottom':
      favorites_nodes.append(self.current_position + self.size)
    elif location[0] == 'top':
      favorites_nodes.append(self.current_position - self.size)

    return favorites_nodes

  def update_step(self):
    neighbors = self.graph[self.current_position]

    neighbors_idx = [n for n, edge in neighbors.items()]
    favorites = self.get_greedy_favorites()
    weights = [ self.advantage if n in favorites else 1 for n in neighbors_idx ]


    if self.q_0 is not None and np.random.rand() < self.q_0:
      new_position = neighbors_idx[np.argmax(weights)]
      # arg_max = np.argwhere(weights == np.amax(weights))
      # new_position = np.random.choice(arg_max.flatten(), 1)[0]
  
    else:
      acu_weight = sum(weights)
      probabilities = np.array(weights)/acu_weight
      # print("[INFO] curren_node: {} nodes: \t {}".format(self.current_position, neighbors_idx))
      # print("[INFO] probabilities: \t {}".format(probabilities))

      # choose an option following the wheel selection algorithm 
      new_position = np.random.choice(neighbors_idx, p = probabilities)
      
    self.current_path.append((self.current_position, new_position))
    self.visited_nodes.append(new_position)
    self.current_position = new_position


class LevyFlightGreedyWalker(ProximityWalker):
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001, omega = 2, advantage = 3):
    # omega clustering exponent

    self.omega = omega # [1-3]

    super().__init__(graph, q_0, reward_tau, advantage)

  def update_step(self):

    # get the neighbors of the current node
    neighbors = self.graph[self.current_position]
    neighbors_idx = [n for n, edge in neighbors.items()]

    # build a list with the possible long range connections
    # here we do not included the neighbors nor the start node
    # or target node
    pos_connections = [ n for n in np.arange(self.start_node + 1, self.target_node) if n not in neighbors_idx]

    long_range_node = np.random.choice(pos_connections)

    dist_current2long_range = get_distance(self.graph.nodes[long_range_node]['pos'],
                                           self.graph.nodes[self.current_position]['pos'],
                                           'euclidean')

    if np.random.rand() < dist_current2long_range ** (- self.omega):
      new_position = long_range_node
      self.current_path.append((self.current_position, new_position))
      self.visited_nodes.append(new_position)
      self.current_position = new_position
    else:
      super().update_step()

class LevyFlightGreedyWalker(GreedyWalker):
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001, omega = 2, advantage = 3):
    # omega clustering exponent

    self.omega = omega # [1-3]

    super().__init__(graph, q_0, reward_tau, advantage)

  def update_step(self):

    # get the neighbors of the current node
    neighbors = self.graph[self.current_position]
    neighbors_idx = [n for n, edge in neighbors.items()]

    # build a list with the possible long range connections
    # here we do not included the neighbors nor the start node
    # or target node
    pos_connections = [ n for n in np.arange(self.start_node + 1, self.target_node) if n not in neighbors_idx]

    long_range_node = np.random.choice(pos_connections)

    dist_current2long_range = get_distance(self.graph.nodes[long_range_node]['pos'],
                                           self.graph.nodes[self.current_position]['pos'],
                                           'euclidean')

    if np.random.rand() < dist_current2long_range ** (- self.omega):
      new_position = long_range_node
      self.current_path.append((self.current_position, new_position))
      self.visited_nodes.append(new_position)
      self.current_position = new_position
    else:
      super().update_step()
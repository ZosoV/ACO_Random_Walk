from utils.measures import get_distance

class Walker():
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001):
    
  
    self.graph = graph
    self.q_0 = q_0
    self.size = graph.size
    self.start_node = 0
    self.target_node = graph.size * graph.size - 1
    self.reward_tau = reward_tau
    self.reset_walk()

  def reset_walk(self):
    self.current_path = []
    self.current_position = self.start_node
    self.visited_nodes = [self.start_node]

  def get_distance_path(self):
    total_distance = 0
    for node1, node2 in self.current_path:
      pos1 = self.graph.nodes[node1]['pos']
      pos2 = self.graph.nodes[node2]['pos']
      total_distance += get_distance(pos1, pos2, 'euclidean')

    return total_distance

  def end_route(self):
    return self.current_position == self.target_node

  def walk(self, num_rand_walks, verbose = True):
    # Create
    distances_list = []

    for i in range(int(num_rand_walks)):
      
      self.reset_walk()

      is_complete = False

      while not is_complete:
        self.update_step()

        is_complete = self.end_route()

      if verbose:
        print("[INFO] n_rw: [{}/{}] len_path: {}".format(i+1, 
                                                 int(num_rand_walks),
                                                 len(self.current_path) ))
      distances_list.append(self.get_distance_path())

    return distances_list

  def reinforce_rw(self):
    # Give a small reward to the edges of the current randown walk
    
    for node1, node2 in self.current_path:

      node2_options = [node1+1, node1-1, node1 - self.graph.size, node1 + self.graph.size]

      if node2 in node2_options:
        self.graph[node1][node2]['pheromone'] += self.reward_tau
        self.graph.nodes[node1]['counter'] += 1

    last_node = self.current_path[-1][1]
    self.graph.nodes[last_node]['counter'] += 1
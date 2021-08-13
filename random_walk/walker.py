from utils.measures import get_distance

class Walker():
  def __init__(self, graph, q_0 = None, reward_tau = 0.0001):
    
  
    self.graph = graph
    self.q_0 = q_0
    self.size = graph.size
    self.start_node = 0
    self.target_node = graph.size * graph.size - 1
    self.reset_walk()

  def reset_walk(self):
    self.current_path = []
    self.current_position = self.start_node
    self.visited_nodes = []

  def get_distance_path(self):
    total_distance = 0
    for node1, node2 in self.current_path:
      pos1 = self.graph.nodes[node1]['pos']
      pos2 = self.graph.nodes[node2]['pos']
      total_distance += get_distance(pos1, pos2, 'euclidean')

    return total_distance

  def end_route(self):
    return self.current_position == self.target_node

  def walk(self, num_rand_walks):
    # Create
    distances_list = []

    for i in range(int(num_rand_walks)):
      
      self.reset_walk()

      is_complete = False

      while not is_complete:
        self.update_step()

        is_complete = self.end_route()

      print("[INFO] n_rw: [{}/{}] len_path: {}".format(i+1, 
                                                 int(num_rand_walks),
                                                 len(self.current_path) ))
      distances_list.append(self.get_distance_path())

    return distances_list
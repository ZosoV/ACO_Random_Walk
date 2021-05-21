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
        self.graph[node1][node2]['pheromone'] += reward

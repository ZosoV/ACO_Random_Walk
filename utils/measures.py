import numpy as np

def get_distance(pos1, pos2, distance):
  x1, y1 = pos1
  x2, y2 = pos2

  if distance == 'euclidean':
    result = np.sqrt((x2-x1)**2 + (y2-y1)**2)
  elif distance == 'manhattan':
    result = np.abs(x2-x1) + np.abs(y2-y1)

  return result

def get_proximity(graph, current_node, neighbor_node, target_node, 
                  mode = 'proximity_1', distance = 'euclidean'):
  """
  Proximity. Calculate the proximity of the neighbor node.
  :param graph:         graph environment
  :param current_node:  index of the current node i
  :param neighbor_node: index of the neihbor node j
  :param target_node:   index of the neihbor node t
  :param mode:          perform the proximity 1 or proximity 2
  :param distance:      used distance to calculate the proximity
  """
  pos_neighbor = graph.nodes[neighbor_node]['pos']
  pos_target = graph.nodes[target_node]['pos']
  pos_current = graph.nodes[current_node]['pos']

  # distance: current node to target
  dis_curr2target = get_distance(pos_current, pos_target, distance)
  
  # distance: neighbor to target
  dis_neig2target = get_distance(pos_neighbor, pos_target, distance)
  
  if neighbor_node == target_node:
    proximity = 1
  else:
    
    if dis_neig2target == 0.0:
        print("Problem with neig2target ditance")

    if mode == 'proximity_1':
      proximity = 1/ dis_neig2target
    elif mode == 'proximity_2':
      proximity = dis_curr2target / dis_neig2target

  return proximity

def normalize_array(array, mode):
  if mode == 'standard':
    mean = np.mean(array)
    std = np.std(array)

    if std != 0.0:
      array = (array - mean) / std

  elif mode == 'l2-norm':
    array = array / np.linalg.norm(array)


  elif mode == 'max-min':
    max = np.amax(array)
    min = np.amin(array)
    if (max - min) != 0.0:
      array = (array - min) / (max - min)


  return array

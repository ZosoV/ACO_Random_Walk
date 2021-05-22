import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import enum

# creating enumerations for status of a each node
# the number associated represent a mark to display
# the environment later in a grid mode
class State(enum.Enum):
    free = 0.9
    obstacle = 0.1
    target = 0.5

#Class to define the environment
class PPGraph(nx.Graph):
  def __init__(self, size, tau_0, filename = None):
    """Define a graph environment given a size
    and tau_0 (initial pheromone).
    The obstacle are loaded from filename
    """
    self.size = size
    self.tau_0 = tau_0
    nx.Graph.__init__(self) 
    self.__create_graph()

  def __create_graph(self):
    """Create a square lattice graph with size x size nodes.
    """

    self.clear() # Remove all the nodes and edges of the last graph
    current_node = 0
    for j in range(self.size - 1, -1, -1):
      for i in range(self.size):  

          #Adding neighbors to the current node
          self.__adding_edges(i,j,current_node, self.tau_0)

          #Adding the node to the network
          self.add_node(current_node, pos=(i,j), state = State.free) 
          current_node += 1

  def __adding_edges(self,i,j,current_node, tau_0):
    """Defines the neighbors per current node"""
    #There are four possible connection
    directions = {
        "up" : current_node - self.size,
        "down" : current_node + self.size,
        "left" : current_node - 1,
        "right" : current_node + 1
    }

    #For border cases of the network, we have to pop some connections
    if i == 0:
      directions.pop("left")
    if i == self.size - 1:
      directions.pop("right")
    if j == 0:
      directions.pop("down")
    if j == self.size - 1:
      directions.pop("up")

    for _, neighbor in directions.items():
      # adding edge      
      self.add_edge(current_node, neighbor, 
                    pheromone = tau_0, 
                    distance = 1)


  #Function to plot the structure of the graph
  def draw_graph(self, node_color='blue', node_size=25, with_labels=False):
    """
    Draw the graph.
        
    node_size: the size of all the nodes
    node_color: the color of all the nodes
    with_labels: True or False to show the ids of the nodes
    """
    fig, ax = plt.subplots()
    ax.set_aspect('equal') #set the x and y axes to the same scale
    pos = nx.get_node_attributes(self, 'pos')
    nx.draw(self, pos, node_color=node_color, node_size=node_size, with_labels=with_labels)

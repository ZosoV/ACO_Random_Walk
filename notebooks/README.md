# Interactive Notebooks 

In this folder, some notebooks that explain some parts of the repository are found. Therefore, if you want to grasp the different ideas and implementation in this research, I recommend exploring this notebook.

The steps that I recommend following are:

1. Review [proximities_testing.ipynb](proximities_testing.ipynb) where it is studied the proximity. This is a relevant heuristic metric that we used in our algorithm.
2. Review [random_walks.ipynb](random_walks.ipynb), where we studied different random walk algorithms in the context of our graph environment.
3. Review [aco_pp.ipynb](aco_pp.ipyn), where we defined the main algorithm and some variants that we implemented to solve the Path Planning problem. This algorithm was based on the state-of-art finding according to [M. Dorigo, M. Birattari and T. Stutzle, "Ant colony optimization"](https://ieeexplore.ieee.org/abstract/document/4129846/), specifically in the algorithm Ant Colony System.

Additional notebooks:

We also have some additional notebooks that were useful during the development of this project.

1. The notebook [aco_tsp.ipynb](aco_tsp.ipynb) contains a simplified version of the Ant Colony Optimization algorithm for solving the Traveling Salesman Problem (TSP) problem.
2. The notebook [random_maze.ipynb](random_maze.ipynb) contains an algorithm to generate random mazes of different sizes. This implementation implements a [Randomized Prim’s Algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) variant, and we based on the following post for developing our version [Fun With Python #1: Maze Generator](https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e)

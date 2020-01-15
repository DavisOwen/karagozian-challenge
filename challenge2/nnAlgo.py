#!/usr/bin/env python
from ast import literal_eval
import sys
import itertools


def find_nearest_neighbors(nodes, radius):
    node_idx = range(1, len(nodes))
    combinations = list(itertools.combinations(node_idx, 2))
    neighbors = [[0] for i in range(len(nodes))]
    for i, j in combinations:
        xi, yi, zi = nodes[i]
        xj, yj, zj = nodes[j]
        dist_squared = (xi-xj)**2 + (yi-yj)**2 + (zi-zj)**2
        if dist_squared <= radius**2:
            neighbors[i][0] += 1
            neighbors[i].append(j)
            neighbors[j][0] += 1
            neighbors[j].append(i)
    neighbors.pop(0)
    return neighbors


# read input file
input_file = open(sys.argv[1], 'r')
radius = int(input_file.readline())
nodes = [None]
for line in input_file.readlines():
    nodes.append(literal_eval(line))
neighbors = find_nearest_neighbors(nodes, radius)
print(neighbors)

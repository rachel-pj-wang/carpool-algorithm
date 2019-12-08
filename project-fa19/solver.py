import os
import random
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import student_utils
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import steinertree


from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""
class Solver:
    def __init__(self):
        self.drop_off = {}

    def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
        """
        Write your algorithm here.
        Input:
            list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
            list_of_homes: A list of homes
            starting_car_location: The name of the starting location for the car
            adjacency_matrix: The adjacency matrix from the input file
        Output:
            A list of locations representing the car path
            A list of (location, [homes]) representing drop-offs
        """
        adj = adjacency_matrix


        s = starting_car_location
        L = list_of_locations
        homes_numbered = [L.index(i) for i in list_of_homes]
        self.homes = homes_numbered
        G = student_utils.adjacency_matrix_to_graph(adj)[0]
        # show_graph(G)
        s = L.index(s)

        H = [L.index(i) for i in list_of_homes] + [s]


        G_steinertree = (steinertree.steiner_tree(G, H))
        directed_steinertree = nx.dfs_tree(G_steinertree, s)

        self.prune_tree(directed_steinertree, s)

        drop_off_locs = set(self.drop_off.values())
        pruned_homes = set(self.drop_off.keys())

        for home in homes_numbered:
            if not (home in pruned_homes):
                drop_off_locs.add(home)

        p,d = nx.floyd_warshall_predecessor_and_distance(G)

        path = (self.nearest_neighbors(drop_off_locs, d, s, p))
        # pos = hierarchy_pos(directed_steinertree, s)
        # nx.draw(directed_steinertree, pos=pos, with_labels=True)
        # plt.show()

        final_dict = {i:[] for i in drop_off_locs}
        for i in homes_numbered:
            if i in drop_off_locs:
                final_dict[i].append(i)
            else:
                final_dict[self.drop_off[i]].append(i)

        with_steiner = path, final_dict
        without_steiner_path = (self.nearest_neighbors(H, d, s, p))
        without_steiner_dict = {i:[i] for i in homes_numbered}
        self.drop_off = {}
        self.prune_tree(directed_steinertree, s)
        # pos = hierarchy_pos(directed_steinertree, s)
        # nx.draw(directed_steinertree, pos=pos, with_labels=True)
        # plt.show()
        drop_off_locs = set(self.drop_off.values())
        pruned_homes = set(self.drop_off.keys())

        for home in homes_numbered:
            if not (home in pruned_homes):
                drop_off_locs.add(home)

        p,d = nx.floyd_warshall_predecessor_and_distance(G)

        path_double_pruned = (self.nearest_neighbors(drop_off_locs, d, s, p))

        final_dict_double_pruned = {i:[] for i in drop_off_locs}
        for i in homes_numbered:
            if i in drop_off_locs:
                final_dict_double_pruned[i].append(i)
            else:
                final_dict_double_pruned[self.drop_off[i]].append(i)

        return min([with_steiner, (without_steiner_path, without_steiner_dict), (path_double_pruned, final_dict_double_pruned)], key= lambda x: cost_of_solution(G, x[0], x[1]))
        # print(with_steiner, '\n', (path_double_pruned, final_dict_double_pruned))
        # return (path_double_pruned, final_dict_double_pruned)
        # return with_steiner
        # if steiner_cost < double_steiner_cost and steiner_cost < without_steiner_cost:
        #     return with_steiner
        # else if (steiner ):
        #
        # else:
        #     return without_steiner_path, without_steiner_dict


    def prune_tree(self, T,s):

        to_remove = []
        for i in T.successors(s):
            x = list(T.successors(i))
            if (not x) and (i in self.homes):
                self.drop_off[i] = s
                to_remove.append(i)
            else:
                self.prune_tree(T, i)
        for i in to_remove:
            T.remove_node(i)






    def constructOutput(path, drop_off_locs, drop_off_dict, H):
        outputString = ""
        outputString += ' '.join(map(str, path)) + '\n'
        outputString += str(len(drop_off_locs)) + '\n'
        final_dict = {i:[] for i in drop_off_locs}
        for i in drop_off_dict.keys():
            final_dict[drop_off_dict[i]].append(i)
        for loc in final_dict.keys():
            if loc in H:
                final_dict[loc].append(loc)
        for i in drop_off_locs:

            outputString += str(i) + ' ' + ' '.join(map(str, final_dict[i])) + '\n'

        return outputString

    def nearest_neighbors(self, L, d, s, p):
        '''
        Returns a greedy path through all the cluster centers
        :param L: the must past through locations
        :param d: all pairs distances
        :param s: start vertex in G
        :param p: all pairs paths
        :return:
        '''
        curr = s
        L = L.copy()
        path = [s]
        while (L):
            next_vertex = min(L, key=lambda x: d[curr][x])
            L.remove(next_vertex)
            temp_path = []
            temp = next_vertex
            while (curr != temp):
                temp_path.append(temp)
                temp = p[curr][temp]
            path += temp_path[::-1]
            curr = next_vertex
        if curr != s:
            next_vertex = s
            curr = p[next_vertex][curr]
            while (curr != next_vertex):
                path.append(curr)
                curr = p[next_vertex][curr]
        return path + [s]

class Node(object):
    def __init__(self, name, children):
        self.name = name
        self.children = children
    def add_child(self, c):
        self.children.append(c)
    def remove(self, c):
        index = 0
        for i in self.children:
            if i.name == c.name:
                del self.children[index]
            index+=1
    def equals(self, node):
        return self.name == node.name

class Tree(object):
    def __init__(self):
        self.content = []

    def addNode(self, name, parent):
        for i in self.content:
            if i == name:
                return
        n = Node(name, [])
        self.content.append(n)
        parent.add_child(self, n)
"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    solver = Solver()
    car_path, drop_offs = solver.solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)

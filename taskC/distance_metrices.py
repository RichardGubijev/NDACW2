import networkx as nx
import multiprocessing as mp
import pickle
import random as rnd
import sys

sys.setrecursionlimit(10000)
N_SEEDS = 10


class FindMarathonDistance:
    def __init__(self, graph, cells: dict, seeds: list):
        self.__graph = graph
        self.__cells = cells
        self.__seeds = seeds
        self.__marathon_paths = {}
        self.__target_distance: int = 42000

    def get_cell_nodes(self, index):
        return self.__cells[self.__seeds[index]]

    @staticmethod
    def is_beginning_end_repeated(path) -> bool:
        return path[0] == path[-1]

    def get_length(self, node1, node2) -> float:
        edge_data = self.__graph.get_edge_data(node1, node2)
        if edge_data is None:
            return 0
        return edge_data[0]['length']

    def get_path_distance(self, path: list) -> float:
        dist = 0
        for node in range(len(path) - 1):
            dist += self.get_length(path[node], path[node + 1])
        return dist

    def process_cell(self, subgraph: nx.MultiDiGraph, seed):
        print("looking over subgraph nodes", len(subgraph.nodes))
        print("finding cycles...")
        cycles = nx.simple_cycles(subgraph, length_bound=100)
        print("searching for marathon lengths...")
        for cycle in cycles:
            if int(self.get_path_distance(cycle)) == self.__target_distance:
                self.__marathon_paths[seed] = cycle
                print("MARATHON!!")
                break
            else:
                print("Not working")
        print(self.__marathon_paths)
        print("-" * 50)

    def find_marathon_paths(self):
        # TODO: multiprocess this
        for i in range(N_SEEDS):
            cell_node = self.get_cell_nodes(i)
            self.process_cell(cell_node, seeds[i])
        return self.__marathon_paths


if __name__ == '__main__':

    with open('../leeds_drive.pickle', 'rb') as f:
        query_place_graph = pickle.load(f)

    all_nodes = list(query_place_graph.nodes)
    print("number of all nodes: ", len(all_nodes))

    # TODO: choose seeds carefully, with respect to k-means yet
    seeds = rnd.choices(all_nodes, k=10)
    cells = nx.voronoi_cells(query_place_graph, seeds, weight='length')

    min_iteration = 0
    min_len = 100000
    for i in range(10):
        length = len(cells[seeds[i]])
        if length < min_len:
            min_len = length
            min_iteration = i

    cell = cells[seeds[min_iteration]]
    subgraph = query_place_graph.subgraph(cell)
    print("number of subgraph nodes: ", len(subgraph.nodes))

    marathon = FindMarathonDistance(query_place_graph, cells, seeds)
    marathon.process_cell(subgraph, seeds[min_iteration])

import networkx as nx
import multiprocessing as mp
import pickle
import random as rnd
import sys
import matplotlib.pyplot as plt
from seeder import get_seeds_with_kmeans

sys.setrecursionlimit(10000)
N_SEEDS = 15


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
            if dist > 42000:
                return 0
        if not self.is_beginning_end_repeated(path):
            dist += self.get_length(path[-1], path[0])
        return dist

    def process_cell(self, subgraph: nx.MultiDiGraph, seed):
        print("looking over subgraph nodes", len(subgraph.nodes))
        print("finding cycles...")
        cycles = nx.simple_cycles(subgraph)
        print("searching for marathon lengths...")
        for cycle in cycles:
            if len(cycle) < 50:
                pass
            path_distance = self.get_path_distance(cycle)
            if int(path_distance) > 20000:
                print("path distance: ", self.get_path_distance(cycle))
                print("cycle length: ", len(cycle))
            if int(path_distance) == 21000:
                print("DO 2 ROUNDS")
            if int(path_distance) == 42000:
                print("DO 1 ROUND")
            if int(self.get_path_distance(cycle)) == self.__target_distance:
                self.__marathon_paths[seed] = cycle
                print("MARATHON!!")
                break
            print("-" * 50)
        print(self.__marathon_paths)
        print("-" * 50)

    def find_marathon_paths(self):
        # TODO: multiprocess this
        for i in range(N_SEEDS):
            cell_node = self.get_cell_nodes(i)
            self.process_cell(cell_node, seeds[i])
        return self.__marathon_paths


def sort_seeds(seeds, cells) -> list:
    return sorted(seeds, key=lambda seed: len(cells[seed]))


if __name__ == '__main__':
    with open('../leeds_drive.pickle', 'rb') as f:
        query_place_graph = pickle.load(f)

    all_nodes = list(query_place_graph.nodes)
    seeds = get_seeds_with_kmeans(query_place_graph, N_SEEDS)
    cells = nx.voronoi_cells(query_place_graph, seeds, weight='length')
    sorted_seeds = sort_seeds(seeds, cells)

    cell1 = cells[sorted_seeds[0]]
    subgraph1 = query_place_graph.subgraph(cell1)
    # cell2 = cells(sorted_seeds[1])
    # subgraph2 = query_place_graph.subgraph(cell2)
    # cell3 = cells(sorted_seeds[2])
    # subgraph3 = query_place_graph.subgraph(cell3)

    marathon = FindMarathonDistance(query_place_graph, cells, seeds)
    marathon.process_cell(subgraph1, sorted_seeds[0])
    plt.show()









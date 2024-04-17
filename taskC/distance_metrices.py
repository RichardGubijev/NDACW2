import networkx as nx
import multiprocess as mp
from multiprocess import Pool
import pickle
import matplotlib.pyplot as plt
import osmnx as ox

N_SEEDS = 10


class FindMarathonDistance:
    def __init__(self, graph, cells: dict, seeds: list, limited_marathons=True):
        self.__graph = graph
        self.__cells = cells
        self.__seeds = seeds
        self.__marathon_paths = []
        self.__target_distance: int = 42000
        self.__limited_marathons = limited_marathons

    def get_marathon_paths(self):
        return self.__marathon_paths

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

    def update_cycle(self, path):
        if not self.is_beginning_end_repeated(path):
            return path + [path[0]]
        return path

    def process_cell(self, subgraph: nx.MultiDiGraph, seed) -> list:
        print("looking over subgraph nodes", len(subgraph.nodes))
        print("finding cycles...")
        cycles = nx.simple_cycles(subgraph)
        print("searching for marathon lengths...")
        marathon_path = None
        for cycle in cycles:
            path_distance = self.get_path_distance(cycle)
            if (int(path_distance) == 10500
                    or int(path_distance) == 21000
                    or int(path_distance) == self.__target_distance):
                print("there is hope!")
                marathon_path = self.__get_marathon_path(cycle, path_distance)
                break
        print("Found a marathon path")
        return marathon_path

    def __get_marathon_path(self, cycle: list, path_distance: float) -> list:
        marathon_path = []
        if int(path_distance) == 10500:
            new_cycle = self.update_cycle(cycle)
            marathon_path = new_cycle + new_cycle[1:] + new_cycle[1:] + new_cycle[1:]
            print("DO 4 ROUNDS")
        elif int(path_distance) == 21000:
            new_cycle = self.update_cycle(cycle)
            marathon_path = new_cycle + new_cycle[1:]
            print("DO 2 ROUNDS")
        elif int(path_distance) == self.__target_distance:
            new_cycle = self.update_cycle(cycle)
            marathon_path = new_cycle
            print("MARATHON!!")
        return marathon_path

    def worker_func(self, i):
        seed = self.__seeds[i]
        subgraph = self.__graph.subgraph(self.__cells[seed])
        return self.process_cell(subgraph, seed)

    def find_marathon_paths(self):
        with Pool(mp.cpu_count()) as pool:
            for marathon_path in pool.imap_unordered(self.worker_func, range(N_SEEDS)):
                if marathon_path is not None:
                    print(marathon_path)
                    self.__marathon_paths.append(marathon_path)
                if len(self.__marathon_paths) >= 3:
                    print("Terminating")
                    pool.terminate()
                    break
        return self.__marathon_paths


if __name__ == '__main__':
    from voronoi_tutorial_helpers import nodes_nearest_seed, get_seed_color, map_node_color_from_seed, \
        map_edge_color_from_node
    from seeder import get_seeds_with_kmeans

    with open('../leeds_drive.pickle', 'rb') as f:
        query_place_graph = pickle.load(f)

    all_nodes = list(query_place_graph.nodes)
    seeds = get_seeds_with_kmeans(query_place_graph, N_SEEDS)
    cells = nx.voronoi_cells(query_place_graph, seeds, weight='length')

    marathon = FindMarathonDistance(query_place_graph, cells, seeds)
    marathon.find_marathon_paths()
    paths = marathon.get_marathon_paths()
    print("-" * 100)
    print(paths)

    colors = ['red', 'blue', 'green']  # add more colors as needed

    black_color = (0.0, 0.0, 0.0, 1.0)
    node_seed_dict = nodes_nearest_seed(query_place_graph, seeds, cells)
    seed_colors = get_seed_color(seeds, black_color)
    node_color_dict = map_node_color_from_seed(query_place_graph, node_seed_dict, seed_colors)
    edge_colors = map_edge_color_from_node(query_place_graph, node_seed_dict, node_color_dict, black_color)

    node_colors = ['r' if node in seeds else 'w' for node in all_nodes]
    fig, ax = ox.plot.plot_graph(query_place_graph, edge_color=edge_colors, node_color=node_colors, bgcolor='k',
                                 show=False, save=True, filepath='nvd.png', node_size=1, figsize=(15, 15))

    for path in paths:
        x = [query_place_graph.nodes[node]['x'] for node in path]
        y = [query_place_graph.nodes[node]['y'] for node in path]
        ax.plot(x, y, color='red', linewidth=2)

    plt.show()

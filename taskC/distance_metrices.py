import networkx as nx
import multiprocessing as mp
import pickle
import random as rnd


class CustomBFS:
    def __init__(self, graph: nx.MultiDiGraph, nodes: set, find_one_circular=True):
        self.__graph = graph
        self.__nodes = nodes
        self.__target_distance: int = 42000
        self.__target_paths = []
        self.__circular_paths = []
        self.__find_one_circular = find_one_circular
        self.__one_circular_path_found = False

    def __bfs_single(self, node, current_path: list, current_distance, start_node, visited) -> None:  # Now returns None
        if current_distance > self.__target_distance:
            return

        if int(current_distance) == self.__target_distance:
            self.__target_paths.append(current_path.copy())
            print("is start equal to end", current_path[0] == current_path[-1])

        visited.add(node)
        for neighbor in self.__graph.neighbors(node):
            # we only check for the nodes inside the cell
            if neighbor not in self.__nodes:
                continue
            # We don't want to revisit already visited nodes
            if neighbor in visited:
                continue
            # Some paths don't have data, so we just continue
            edge_data = self.__graph.get_edge_data(neighbor, node)
            if edge_data is None:
                continue
            distance = edge_data[0]['length']
            # We check if there exists a circular path, if so we append it to the circular paths
            if start_node == neighbor and int(distance) == self.__target_distance:
                self.__circular_paths.append(start_node)
                print("circular found yesss")
                if self.__find_one_circular:
                    self.__one_circular_path_found = True
                    break
                continue

            # we do BFS
            current_path.append(neighbor)
            current_distance += distance
            self.__bfs_single(neighbor, current_path, current_distance, start_node, visited)
            current_path.pop()
            current_distance -= distance

        visited.remove(node)

    def bfs(self):
        for node in self.__nodes:
            if self.__one_circular_path_found:
                break
            self.__bfs_single(node, [node], 0, node, set())
        return self.__target_paths, self.__circular_paths


N_SEEDS = 10

with open('../my_graph.pickle', 'rb') as f:
    query_place_graph = pickle.load(f)

all_nodes = list(query_place_graph.nodes)

# TODO: choose seeds carefully, with respect to idk yet
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
custom_dfs = CustomBFS(query_place_graph, cell)
custom_dfs.bfs()

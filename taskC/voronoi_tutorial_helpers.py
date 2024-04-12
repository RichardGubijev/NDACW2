# All methods are taken from week_6_sol.ipynb,
# some methods are changed slightly to fit my implementation

import networkx as nx
import osmnx as ox


def nearest_from_list(node_distances):
    return sorted(node_distances, key=lambda node_length: node_length[1])[0] \
        if len(node_distances) > 0 else None


def map_node_color_from_seed(graph, node_seed_dict, seed_colors):
    return {node: seed_colors[node_seed_dict[node]] for node in graph.nodes}


def nearest_seed(node, distances, seeds):
    seed_distances = [(seed, distances[seed][node]) \
                      for seed in seeds if node in distances[seed]]
    return nearest_from_list(seed_distances)


def nearest_for_edge(edge):
    nearest_to_ends_all = [nearest_seed(edge[0]), nearest_seed(edge[1])]
    nearest_to_ends = [distance for distance in nearest_to_ends_all if distance]
    return nearest_from_list(nearest_to_ends)


def get_colours(n_seeds: int):
    return ox.plot.get_colors(n_seeds)


def colour_for_seed_distance(seed, colours, seeds):
    return colours[seeds.index(seed[0])]


def nodes_nearest_seed(graph, seeds, cells):
    cells_inverse = {v: key for key, value in cells.items() for v in value}  # inverse cells dict
    return cells_inverse


def get_seed_color(seeds, black_color):
    seed_colors = dict(zip(seeds, ox.plot.get_colors(len(seeds))))  # {seed: seed's mapped color}
    seed_colors['unreachable'] = black_color
    return seed_colors


def map_edge_color_from_node(graph, node_seed_dict, node_colors, black_color):
    edge_colors = []
    for i, e in enumerate(graph.edges):
        color_pair = [node_colors[e[0]], node_colors[e[1]]]
        if black_color in color_pair:  # unreachable
            color_pair.remove(black_color)
            edge_colors.append(color_pair[0])
        elif color_pair[0] == color_pair[1]:
            edge_colors.append(color_pair[0])
        else:
            len_0 = nx.shortest_path_length(graph, node_seed_dict[e[0]], e[0], weight='length')
            len_1 = nx.shortest_path_length(graph, node_seed_dict[e[1]], e[1], weight='length')
            if len_0 <= len_1:  # or discuss on equality cases
                edge_colors.append(color_pair[0])
            else:
                edge_colors.append(color_pair[1])
    return edge_colors
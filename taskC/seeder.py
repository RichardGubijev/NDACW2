import math

import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import KMeans
import networkx as nx
import numpy as np
import osmnx as ox

def get_seeds_kMeans(graph, num_seeds: int):
    # 2. Extract node coordinates
    coords = [(node, data['x'], data['y']) for node, data in graph.__nodes(data=True)]
    gdf_nodes = gpd.GeoDataFrame(coords, columns=['node_id', 'x', 'y'])

    # 3. Apply K-means clustering
    kmeans = KMeans(n_clusters=num_seeds)
    kmeans.fit(gdf_nodes[['x', 'y']])

    # 4. Extract cluster centroids as seeds
    unaligned_seeds = [Point(x, y) for x, y in kmeans.cluster_centers_]

    # 5. Find closest nodes on the road network
    closest_seeds = []
    for seed in unaligned_seeds:
        distance, closest_node = nx.closest_node(graph, seed)  # Find distance along with the node
        closest_point_on_road = nx.shortest_path(graph, seed, closest_node, weight='length')[1]
        closest_seeds.append(Point(closest_point_on_road[0], closest_point_on_road[1]))

    return closest_seeds

# def eucledian_distance(point1, point2):
#     return math.sqrt(point2**2)
#
# def closest_node(G, node, metric='euclidean'):
#     """Find the node in graph G closest to 'node' based on a specified metric (default: Euclidean)"""
#     distances = [(n, ) for n in G.nodes()]
#     return min(distances, key=lambda x: x[1])[0]

def get_nearest_edge(G, point):
    # Get all edges in the graph
    gdf = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
    graph_edges = gdf[["geometry", "u", "v"]].values.tolist()

    # Compute the Euclidean distance from the coordinates to each edge
    edges_with_distances = [
        (graph_edge, ox.Point(tuple(reversed(point))).distance(graph_edge[0]))
        for graph_edge in graph_edges
    ]

    # Sort edges based on distance
    edges_with_distances.sort(key=lambda x: x[1])

    # Return the closest edge (geometry and u, v nodes)
    return edges_with_distances[0]

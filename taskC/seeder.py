import geopandas as gpd
from sklearn.cluster import KMeans
import osmnx as ox
import pickle
import networkx as nx


def get_seeds_with_kmeans(graph: nx.MultiDiGraph, num_seeds: int):
    coords = [(node, data['x'], data['y']) for node, data in graph.nodes(data=True)]
    gdf_nodes = gpd.GeoDataFrame(coords, columns=['node_id', 'x', 'y'])

    kmeans = KMeans(n_clusters=num_seeds)
    kmeans.fit(gdf_nodes[['x', 'y']])

    unaligned_seeds = [(x, y) for x, y in kmeans.cluster_centers_]
    return __align_seeds(graph, unaligned_seeds)


def __align_seeds(graph: nx.MultiDiGraph, unaligned_seeds: list[tuple]) -> list:
    nearest_node_ids = []
    for seed in unaligned_seeds:
        lat, lon = seed
        nearest_node_ids.append(ox.nearest_nodes(graph, lat, lon, return_dist=False))
    return nearest_node_ids


if __name__ == '__main__':
    N_SEEDS = 10

    with open('../leeds_drive.pickle', 'rb') as f:
        query_place_graph = pickle.load(f)

    all_nodes = list(query_place_graph.nodes)
    seeds = get_seeds_with_kmeans(query_place_graph, N_SEEDS)




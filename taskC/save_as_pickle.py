import osmnx as ox
import pickle
N_SEEDS = 10
trondheim_graph = ox.graph_from_place('Trondheim, Norway', network_type='drive')
leeds_graph = ox.graph_from_place('Leeds, United Kingdom', network_type='drive')


with open('trondheim.pickle', 'wb') as f:
    pickle.dump(trondheim_graph, f)

with open('leeds.pickle', 'wb') as f:
    pickle.dump(leeds_graph, f)
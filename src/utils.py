import numpy as np
from scipy.spatial.distance import cdist

def load_data(file_path):
    """加载 VRP 数据"""
    coords, demands, capacity = [], [], 0
    with open(file_path, 'r') as file:
        lines = file.readlines()
        in_node_section, in_demand_section = False, False
        for line in lines:
            if line.startswith("CAPACITY"):
                capacity = int(line.split(":")[1].strip())
            elif line.startswith("NODE_COORD_SECTION"):
                in_node_section = True
            elif line.startswith("DEMAND_SECTION"):
                in_node_section = False
                in_demand_section = True
            elif line.startswith("DEPOT_SECTION"):
                break
            elif in_node_section:
                _, x, y = map(float, line.strip().split())
                coords.append((x, y))
            elif in_demand_section:
                _, demand = map(int, line.strip().split())
                demands.append(demand)
    return np.array(coords), np.array(demands), capacity

def compute_distance_matrix(coords):
    """计算距离矩阵"""
    return cdist(coords, coords, metric='euclidean')

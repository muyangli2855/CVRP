from scipy.spatial.distance import cdist

def clarke_wright_savings(distance_matrix, demands, capacity):
    """Clarke-Wright Savings 算法"""
    num_nodes = len(demands)
    routes = [[i] for i in range(1, num_nodes)]
    vehicle_loads = demands[1:].tolist()

    savings = []
    for i in range(1, num_nodes):
        for j in range(i + 1, num_nodes):
            savings.append((distance_matrix[0, i] + distance_matrix[0, j] - distance_matrix[i, j], i, j))
    savings.sort(reverse=True, key=lambda x: x[0])

    for _, i, j in savings:
        route_i = next((r for r in routes if i in r), None)
        route_j = next((r for r in routes if j in r), None)
        if route_i != route_j and sum(demands[node] for node in route_i + route_j) <= capacity:
            route_i.extend(route_j)
            routes.remove(route_j)

    return routes

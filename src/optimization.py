def optimize_tsp_route(route, distance_matrix):
    """贪心算法优化 TSP 路径"""
    if len(route) <= 1:
        return route

    current_node = 0  # depot
    unvisited = set(route)
    optimized_route = []

    while unvisited:
        next_node = min(unvisited, key=lambda x: distance_matrix[current_node, x])
        optimized_route.append(next_node)
        unvisited.remove(next_node)
        current_node = next_node

    return optimized_route

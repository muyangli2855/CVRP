import numpy as np

def evaluate_routes(routes, distance_matrix, demands, capacity):
    """评估生成的路径"""
    total_cost, total_loads = 0, []
    for route in routes:
        cost, load = 0, 0
        full_route = [0] + route + [0]
        for i in range(len(full_route) - 1):
            cost += distance_matrix[full_route[i], full_route[i + 1]]
            load += demands[full_route[i]]
        total_cost += cost
        total_loads.append(load)

    return {
        "Total Cost": total_cost,
        "Vehicle Loads": total_loads,
        "Average Utilization": np.mean(total_loads) / capacity
    }

def save_solution_to_file(routes, distance_matrix, output_path):
    """保存解决方案到文件"""
    total_cost = 0
    with open(output_path, 'w') as f:
        for i, route in enumerate(routes, 1):
            route_cost = 0
            full_route = [0] + route + [0]
            for j in range(len(full_route) - 1):
                route_cost += distance_matrix[full_route[j], full_route[j + 1]]
            total_cost += route_cost
            route_str = " ".join(map(str, route))
            f.write(f"Route #{i}: {route_str}\n")
        f.write(f"Cost {int(total_cost)}\n")
    return total_cost

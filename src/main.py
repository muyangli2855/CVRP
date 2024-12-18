import os
import time
from src.utils import load_data, compute_distance_matrix
from src.clustering import kmeans_clustering
from src.routing import clarke_wright_savings
from src.optimization import optimize_tsp_route
from src.evaluation import save_solution_to_file

def load_official_cost(solution_path):
    """加载官方提供的成本"""
    with open(solution_path, 'r') as file:
        for line in file:
            if line.startswith("Cost"):
                return float(line.split()[1])
    return None

def analyze_results(results):
    """分析实验结果并生成报告"""
    cost_improvement = [
        ((result['Baseline Cost'] - result['Clustered Cost']) / result['Baseline Cost']) * 100
        for result in results
    ]
    average_cost_improvement = sum(cost_improvement) / len(cost_improvement)

    time_increase = [
        ((result['Clustered Time'] - result['Baseline Time']) / result['Baseline Time']) * 100
        for result in results
    ]
    average_time_increase = sum(time_increase) / len(time_increase)

    official_comparison = [
        {
            "Instance": result["Instance"],
            "Baseline Deviation": ((result["Baseline Cost"] - result["Official Cost"]) / result["Official Cost"]) * 100,
            "Clustered Deviation": ((result["Clustered Cost"] - result["Official Cost"]) / result["Official Cost"]) * 100,
        }
        for result in results
    ]

    print(f"--- Analysis Report ---")
    print(f"Average Cost Improvement: {average_cost_improvement:.2f}%")
    print(f"Average Time Increase: {average_time_increase:.2f}%\n")

    print("--- Official Cost Comparison ---")
    for comparison in official_comparison:
        print(f"{comparison['Instance']}: Baseline Deviation = {comparison['Baseline Deviation']:.2f}%, "
              f"Clustered Deviation = {comparison['Clustered Deviation']:.2f}%")

def main():
    data_dir = '../data/B'
    output_dir = '../outputs/B'
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.vrp'):
            instance_name = filename[:-4]
            instance_path = os.path.join(data_dir, filename)
            solution_path = os.path.join(data_dir, f"{instance_name}.sol")
            output_path_baseline = os.path.join(output_dir, f"{instance_name}_baseline.mysol")
            output_path_clustered = os.path.join(output_dir, f"{instance_name}_clustered.mysol")

            coords, demands, capacity = load_data(instance_path)
            distance_matrix = compute_distance_matrix(coords)

            # Load official cost
            official_cost = load_official_cost(solution_path)

            # Baseline: direct solving
            start_time = time.time()
            baseline_routes = clarke_wright_savings(distance_matrix, demands, capacity)
            baseline_cost = save_solution_to_file(baseline_routes, distance_matrix, output_path_baseline)
            baseline_time = time.time() - start_time

            # Clustering-based optimization
            start_time = time.time()
            labels, _ = kmeans_clustering(coords[1:], num_clusters=5)
            clustered_routes = [optimize_tsp_route(route, distance_matrix) for route in clarke_wright_savings(distance_matrix, demands, capacity)]
            clustered_cost = save_solution_to_file(clustered_routes, distance_matrix, output_path_clustered)
            clustered_time = time.time() - start_time

            # Record results
            results.append({
                "Instance": instance_name,
                "Official Cost": official_cost,
                "Baseline Cost": baseline_cost,
                "Baseline Time": baseline_time,
                "Clustered Cost": clustered_cost,
                "Clustered Time": clustered_time
            })

    # Print experiment results
    print("\n--- Results ---")
    for result in results:
        print(result)

    # Analyze results and generate report
    analyze_results(results)

if __name__ == "__main__":
    main()

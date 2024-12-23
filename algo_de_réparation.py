import numpy as np

def parse_instance(file_path):
    """
    Parse an MKP instance from the given file.

    Arguments:
    file_path -- path to the file containing the instance

    Returns:
    profits -- list of profits for each project
    weights -- 2D list where weights[i][j] is the consumption of resource i by project j
    capacities -- list of available capacities for each resource
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract number of projects and resources from the first instance
    n_projects, n_resources, _ = map(int, lines[1].split())

    # Extract profits
    profits = list(map(int, lines[2].split()))

    # Extract weights (resource consumptions)
    weights = []
    for i in range(n_resources):
        weights.append(list(map(int, lines[3 + i].split())))

    # Extract capacities
    capacities = list(map(int, lines[3 + n_resources].split()))

    return profits, weights, capacities

def repair_heuristic_knapsack(profits, weights, capacities):
    """
    Repair heuristic with performance guarantee for multidimensional knapsack problem.

    Arguments:
    profits -- list of profits for each project
    weights -- 2D list, where weights[i][j] is the weight of project j in dimension i
    capacities -- list of available capacities for each dimension

    Returns:
    solution -- list indicating if each project is included (1) or not (0)
    total_profit -- total profit of the solution
    """
    n_projects = len(profits)
    n_resources = len(capacities)

    # Initial solution: include all projects
    solution = [1] * n_projects
    current_weights = [sum(weights[i][j] for j in range(n_projects)) for i in range(n_resources)]

    # Check if the initial solution is feasible
    feasible = all(current_weights[i] <= capacities[i] for i in range(n_resources))

    if not feasible:
        # Sort projects by profit-to-weight ratio
        ratios = [(profits[j] / sum(weights[i][j] for i in range(n_resources)), j) for j in range(n_projects)]
        ratios.sort(reverse=True)

        # Remove projects until the solution is feasible
        for ratio, j in ratios:
            if all(current_weights[i] <= capacities[i] for i in range(n_resources)):
                break
            solution[j] = 0
            for i in range(n_resources):
                current_weights[i] -= weights[i][j]

    total_profit = sum(profits[j] for j in range(n_projects) if solution[j] == 1)

    return solution, total_profit

# Test the heuristic
if __name__ == "__main__":
    # Parse the instance from the file
    file_path = "instances/mknapcb5.txt"
    profits, weights, capacities = parse_instance(file_path)

    # Apply the constructive heuristic
    solution, total_profit = repair_heuristic_knapsack(profits, weights, capacities)

    print("Solution:", solution)
    print("Total Profit:", total_profit)

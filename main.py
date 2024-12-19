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

def constructive_knapsack(profits, weights, capacities):
    """
    Constructive heuristic for multidimensional knapsack problem.

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

    solution = [0] * n_projects
    current_weights = [0] * n_resources

    # Iterate over projects in random order
    indices = list(range(n_projects))
    np.random.shuffle(indices)

    for j in indices:
        # Check if adding project j respects all capacity constraints
        if all(current_weights[i] + weights[i][j] <= capacities[i] for i in range(n_resources)):
            solution[j] = 1
            for i in range(n_resources):
                current_weights[i] += weights[i][j]

    total_profit = sum(profits[j] * solution[j] for j in range(n_projects))
    return solution, total_profit

# Test the heuristic
if __name__ == "__main__":
    # Parse the instance from the file
    file_path = "mknapcb3.txt"
    profits, weights, capacities = parse_instance(file_path)

    # Apply the constructive heuristic
    solution, total_profit = constructive_knapsack(profits, weights, capacities)

    print("Solution:", solution)
    print("Total Profit:", total_profit)

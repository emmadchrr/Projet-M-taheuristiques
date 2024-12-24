import numpy as np
import time

def parse_instance(file_path):
    """
    Parse an MKP instance from the given file.

    Arguments:
    file_path -- path to the file containing the instance

    Returns:
    instances -- list of tuples (profits, weights, capacities) for each instance
        profits -- list of profits for each project
        weights -- 2D list where weights[i][j] is the consumption of resource i by project j
        capacities -- list of available capacities for each resource
    """
    with open(file_path, 'r') as file:
        lines = [line for line in file.readlines() if line.strip()] # only non-empty lines
    
    n_instances = int(lines[0])
    instances = []
    index = 1

    for _ in range(n_instances):
        # Extract number of projects and resources
        n_projects, m_resources, v_opt = lines[index].split()
        n_projects = int(n_projects)
        m_resources = int(m_resources)
        v_opt = float(v_opt) if '.' in v_opt else int(v_opt)
        index += 1

        # Extract profits
        profits = list(map(float, lines[index].split()))
        index += 1
        # Handle case where profits span multiple lines
        while len(profits) < n_projects:
            if index >= len(lines):
                raise IndexError("Unexpected end of file while reading profits.")
            profits.extend(map(float, lines[index].split()))
            index += 1

        # Extract weights
        resources_consumed = []
        for i in range(m_resources):
            if index >= len(lines):
                raise IndexError("Unexpected end of file while reading resource weights.")
            resource_line = list(map(int, lines[index].split()))
            index += 1
            # Handle case where resource weights span multiple lines
            while len(resource_line) < n_projects:
                if index >= len(lines):
                    raise IndexError("Unexpected end of file while reading resource weights.")
                resource_line.extend(map(int, lines[index].split()))
                index += 1
            resources_consumed.append(resource_line)

        # Extract capacities
        if index >= len(lines):
            raise IndexError("Unexpected end of file while reading capacities.")
        resources_available = list(map(int, lines[index].split()))
        index += 1
        # Handle case where resource availability span multiple lines
        while len(resources_available) < m_resources:
            if index >= len(lines):
                raise IndexError("Unexpected end of file while reading capacities.")
            resources_available.extend(map(int, lines[index].split()))
            index += 1

        # Add the instance to the list
        instance = {
            "n_projects": n_projects,
            "m_resources": m_resources,
            "optimal_value": v_opt,
            "profits": profits,
            "resources_consumed": resources_consumed,
            "resources_available": resources_available
        }
        instances.append(instance)

    return instances

def surrogate_relaxation(instance):
    """
    Surrogate Relaxation
    """
    n_projects = instance["n_projects"]
    m_resources = instance["m_resources"]
    resources_consumed = instance["resources_consumed"]

    # Calculate weights for the surrogate relaxation
    surrogate_weights = np.zeros(n_projects)
    for j in range(n_projects):
        surrogate_weights[j] = sum(resources_consumed[i][j] for i in range(m_resources))

    total_resources_available = sum(instance["resources_available"])

    return surrogate_weights, total_resources_available

def glouton_heuristic(profits, surrogate_weights, total_resources_available):
    """
    Apply a greedy heuristic based on the ratio ci/ai on an instance obtained by surrogate relaxation
    """
    n_projects = len(profits)
    profits = np.array(profits)
    ratios = profits / surrogate_weights
    sorted_idx = np.argsort(-ratios)  # idx from best to worst ratio

    solution = np.zeros(n_projects, dtype=int)
    capacity = total_resources_available

    for idx in sorted_idx:
        if capacity >= surrogate_weights[idx]:
            solution[idx] = 1
            capacity -= surrogate_weights[idx]

    return solution, sorted_idx

def repair_heuristic(instance, glouton_solution, sorted_idx):
    """
    Given an initial solution obtained by a greedy heuristic, here for the surrogate relaxation.
    But NOT feasible for the original multidimensional knapsack problem
    => Repair by removing the item with the worst ratio

    :param glouton_solution: Initial solution obtained by greedy heuristic for the surrogate relaxation
    :param instance: Dictionary containing the instance data (output of 'read_instances').
    :return: Repaired solution feasible for the original MDKP
    """
    resources_consumed = instance["resources_consumed"]
    resources_available = instance["resources_available"]
    solution = glouton_solution.copy()
    sorted_idx = sorted_idx.copy()

    # Calculate the total resource consumption for the initial solution
    total_consumption = np.dot(resources_consumed, solution)
    idx = 1

    # While the solution does not respect the capacity constraints
    while np.any(total_consumption > resources_available):
        # Select the project that was not already at solution[project] = 0 with the worst ratio
        bad_ratio_idx = sorted_idx[-idx]
        if solution[bad_ratio_idx] == 0:
            idx += 1
            bad_ratio_idx = sorted_idx[-idx]

        # Remove the project with the worst ratio
        solution[bad_ratio_idx] = 0

        # Recalculate the total resource consumption
        total_consumption = np.dot(resources_consumed, solution)
        idx +=1
    
    return solution
 
def solve_mdkp_with_repair(file_path):
    """
    Solve MDKP instances with a repair approach.
    
    :param file_path: Path to the file containing the instances.
    :return: List of repaired solutions for each instance, with the found upper bound value, resolution time, and gap to the optimal value.
    """
    instances = parse_instance(file_path)
    solutions = {}
    for i, instance in enumerate(instances, start=1):
        start_time = time.time()
        
        # Surrogate Relaxation
        surrogate_weights, total_resources_available = surrogate_relaxation(instance)

        # Apply the greedy heuristic to obtain an initial solution for the surrogate relaxation
        initial_solution, sorted_idx = glouton_heuristic(instance["profits"], surrogate_weights, total_resources_available)
        
        # Repair the solution to make it feasible for the initial MDKP
        repaired_solution = repair_heuristic(instance, initial_solution, sorted_idx)
        
        # Calculate the found upper bound value
        majorant_value = np.dot(repaired_solution, instance["profits"])
        
        # Calculate the gap to the optimal value
        optimal_value = instance["optimal_value"]
        gap = abs(optimal_value - majorant_value)
        
        # Resolution time
        resolution_time = time.time() - start_time
        
        solutions[f'instance_{i}'] = {
            "solution": repaired_solution,
            "majorant_value": majorant_value,
            "resolution_time": resolution_time,
            "gap": gap
        }

    return solutions

# Test the heuristic
if __name__ == "__main__":
    # Parse the instance from the file
    file_path = "instances/mknapcb9.txt"
    instances = parse_instance(file_path)

    # Solve the instances with the repair heuristic
    solutions = solve_mdkp_with_repair(file_path)
    for instance_id, solution in solutions.items():
        # print(f'{instance_id}: {solution}')
        print(f'{instance_id}: majorant_value = {solution["majorant_value"]}')  # Only display the objective function values
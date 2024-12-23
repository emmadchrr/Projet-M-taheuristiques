#%%
import numpy as np
import time

def read_instances(file_path):
    """
    Lit les instances du problème MDKP à partir d'un fichier formaté, en ignorant les lignes vides.
    
    :param file_path: Chemin vers le fichier contenant les instances.
    :return: Liste de dictionnaires représentant les instances.
    """
    instances = []
    
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # Supprime les lignes vides et les espaces inutiles
    
    num_instances = int(lines[0])  # Première ligne : nombre d'instances
    current_line = 1  # Pointeur pour lire les lignes

    for _ in range(num_instances):
        # Lire les informations générales de l'instance
        try:
            parts = list(map(float, lines[current_line].split()))
            if len(parts) != 3:
                raise ValueError(f"Erreur de format à la ligne {current_line + 1}: {lines[current_line]}")
            n_projects, m_resources, optimal_value = parts
            n_projects = int(n_projects)  # Convertir n_projects et m_resources en entier
            m_resources = int(m_resources)
            optimal_value = float(optimal_value)  # On garde optimal_value comme float
        except ValueError:
            raise ValueError(f"Erreur de format à la ligne {current_line + 1}: {lines[current_line]}")
        
        current_line += 1

        # Lire les gains des projets
        gains = []
        while len(gains) < n_projects:
            gains.extend(map(float, lines[current_line].split()))
            current_line += 1
        
        if len(gains) != n_projects:
            raise ValueError(f"Erreur : Nombre de gains ({len(gains)}) ne correspond pas au nombre de projets ({n_projects}) après lecture des lignes nécessaires.")
        
        # Lire les quantités de ressources consommées par projet
        resources_consumed = []
        for _ in range(m_resources):
            resource_line = []
            while len(resource_line) < n_projects:
                resource_line.extend(map(int, lines[current_line].split()))
                current_line += 1
            resources_consumed.append(resource_line)

        # Lire les quantités de ressources disponibles
        resources_available = list(map(int, lines[current_line].split()))
        current_line += 1
        
        # Ajouter l'instance à la liste
        instance = {
            "n_projects": n_projects,
            "m_resources": m_resources,
            "optimal_value": optimal_value,
            "gains": gains,
            "resources_consumed": resources_consumed,
            "resources_available": resources_available
        }
        instances.append(instance)

    return instances


def repair_solution(solution, instance):
    """
    Répare une solution initiale pour qu'elle respecte les contraintes du MDKP.
    
    :param solution: Liste binaire indiquant si un projet est sélectionné (1) ou non (0).
    :param instance: Dictionnaire contenant les données de l'instance (output de `read_instances`).
    :return: Solution réparée respectant les contraintes.
    """
    num_projects = instance["n_projects"]
    num_resources = instance["m_resources"]
    optimal_value = instance["optimal_value"]
    gains = np.array(instance["gains"])
    resource_consumption = np.array(instance["resources_consumed"])
    resource_availability = np.array(instance["resources_available"])
    
    # Vérifier la consommation actuelle
    current_consumption = np.dot(resource_consumption, solution)
    
    while not np.all(current_consumption <= resource_availability):
        # Trouver les indices des projets sélectionnés
        selected_projects = np.where(solution == 1)[0]
        
        # Calculer le rapport gain / consommation pour chaque projet sélectionné
        ratios = []
        for project in selected_projects:
            # Éviter la division par zéro
            total_consumption = np.sum(resource_consumption[:, project])
            ratio = gains[project] / total_consumption if total_consumption > 0 else 0
            ratios.append((project, ratio))
        
        # Trouver le projet avec le pire ratio
        worst_project = min(ratios, key=lambda x: x[1])[0]
        
        # Retirer ce projet de la solution
        solution[worst_project] = 0
        
        # Recalculer la consommation
        current_consumption = np.dot(resource_consumption, solution)
    
    return solution

def solve_mdkp_with_repair(file_path):
    """
    Résout les instances MDKP avec une approche par réparation.
    
    :param file_path: Chemin vers le fichier contenant les instances.
    :return: Liste des solutions réparées pour chaque instance, avec la valeur du majorant trouvé, le temps de résolution et le saut à la valeur optimale.
    """
    instances = read_instances(file_path)
    solutions = []
    
    for instance in instances:
        start_time = time.time()
        
        # Initialiser une solution naïve : sélectionner tous les projets
        initial_solution = np.ones(instance["n_projects"], dtype=int)
        
        # Réparer la solution pour qu'elle devienne faisable
        repaired_solution = repair_solution(initial_solution, instance)
        
        # Calculer la valeur du majorant trouvé
        majorant_value = np.dot(repaired_solution, instance["gains"])
        
        # Calculer le saut à la valeur optimale
        optimal_value = instance["optimal_value"]
        gap = abs(optimal_value - majorant_value)
        
        # Temps de résolution
        resolution_time = time.time() - start_time
        
        solutions.append({
            "solution": repaired_solution,
            "majorant_value": majorant_value,
            "resolution_time": resolution_time,
            "gap": gap
        })
    
    return solutions

#%%
#%%
if __name__ == "__main__":
    instances = read_instances("instances/mknap1.txt")
    solutions = solve_mdkp_with_repair("instances/mknap1.txt")
    print(instances)
    print(solutions)
#%%
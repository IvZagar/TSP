from tsp_context import *
from tsp_generate_tree import *
import random


def get_random_node(root):
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return random.choice(nodes)


# OK
def calculate_depth(root):
    if root is None:
        return -1
    else:
        left_depth = calculate_depth(root.left)
        right_depth = calculate_depth(root.right)
        return max(left_depth, right_depth) + 1


def crossover(tree1, tree2):
    original_tree1 = deepcopy(tree1)
    original_tree2 = deepcopy(tree2)

    node1 = get_random_node(original_tree1)
    node2 = get_random_node(original_tree2)

    if node1.value in function_set and node2.value in function_set:
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right
    else:
        return original_tree1, original_tree2

    if tree1 == original_tree1 and tree2 == original_tree2:
        return original_tree1, original_tree2

    if calculate_depth(original_tree1) > 8 or calculate_depth(original_tree2) > 8:
        crossover(original_tree1, original_tree2)
    mutate_tree(original_tree1)
    mutate_tree(original_tree2)
    return original_tree1, original_tree2


def mutate_tree(node, mutation_rate=0.05, max_depth=8, current_depth=0):
    if current_depth >= max_depth:
        return  # Stop the recursion if maximum depth is reached

    if random.random() < mutation_rate:
        if node.left or node.right:
            if random.random() < mutation_rate:
                if node.value in function_set:
                    node.value = random.choice(function_set)
                else:
                    mutate_tree(
                        random.choice([node.left, node.right]),
                        mutation_rate,
                        max_depth,
                        current_depth + 1,
                    )
        else:
            if node.value in function_set:
                node.value = random.choice(function_set)

    if node.left:
        mutate_tree(node.left, mutation_rate, max_depth, current_depth + 1)
    if node.right:
        mutate_tree(node.right, mutation_rate, max_depth, current_depth + 1)

    return node


def calculate_fitness(route, points):
    total_distance = 0

    for i in range(len(route) - 1):
        point1 = points[route[i]]
        point2 = points[route[i + 1]]
        total_distance += tsp_calculate_distance(point1, point2)

    return total_distance


def deepcopy(root):
    if root is None:
        return None
    else:
        new_root = Node(root.value)
        new_root.left = deepcopy(root.left)
        new_root.right = deepcopy(root.right)
        return new_root


def modified_tournament_selection_and_crossover(
    population, points, mutation_rate, fitnesses, k
):
    population_size = len(population)
    ran = population_size - 1

    enumerated_solutions = list(enumerate(fitnesses))

    # Sort the list in descending order based on values
    sorted_solutions = sorted(enumerated_solutions, key=lambda x: x[1], reverse=False)

    # Take the first two items (highest values) and extract their indices
    highest_indices = [item[0] for item in sorted_solutions[:2]]

    print(highest_indices)
    new_population = []
    new_population.append(population[highest_indices[0]])
    new_population.append(population[highest_indices[1]])
    while population_size - 2:
        tournament_indices = []
        j = 3
        while j > 0:
            indice = random.randint(0, ran)
            if indice not in tournament_indices:
                tournament_indices.append(indice)
                j -= 1
        maximum = 0
        maximum_fitness = 0
        for indice in tournament_indices:
            if fitnesses[indice] > maximum_fitness:
                maximum_fitness = fitnesses[indice]
                maximum = indice
        tournament_indices.remove(maximum)
        (parent1, parent2) = (
            population[tournament_indices[0]],
            population[tournament_indices[1]],
        )

        child1, child2 = crossover(parent1[1], parent2[1])

        chosen_child = random.choice([child1, child2])

        if chosen_child not in [p[1] for p in new_population] and tsp_route_finder(
            points, k, chosen_child
        ) not in [p[0] for p in new_population]:
            new_population.append(
                (tsp_route_finder(points, k, chosen_child), chosen_child)
            )
            population_size -= 1

    new_fitnesses = []
    for pop in new_population:
        new_fitnesses.append(calculate_fitness(pop[0], points))

    return new_population, new_fitnesses

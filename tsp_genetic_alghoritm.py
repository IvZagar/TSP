from tsp_context import *
from tsp_generate_tree import *
import random


def calculate_fitness(route, points):
    total_distance = 0

    for i in range(len(route) - 1):
        point1 = points[route[i]]
        point2 = points[route[i + 1]]
        total_distance += tsp_calculate_distance(point1, point2)

    return total_distance


def is_compatible(node1, node2):
    return (node1.value in operators and node2.value in operators) or (
        node1.value in terminals and node2.value in terminals
    )


def find_compatible_subtree(node, compatible_with):
    compatible_subtrees = [
        child for child in node.children if is_compatible(child, compatible_with)
    ]
    return random.choice(compatible_subtrees) if compatible_subtrees else None


def tree_depth(node):
    if not node.children:
        return 1
    return 1 + max(tree_depth(child) for child in node.children)


def mutate_tree(node, mutation_rate, max_depth=8, current_depth=0):
    if current_depth >= max_depth:
        return  # Stop the recursion if maximum depth is reached

    if random.random() < mutation_rate:
        if node.children:
            mutate_tree(
                random.choice(node.children),
                mutation_rate,
                max_depth,
                current_depth + 1,
            )
        else:
            if node.value in operators:
                node.value = random.choice(list(operators.keys()))
            elif node.value in terminals:
                node.value = random.choice(terminals)

    for child in node.children:
        mutate_tree(child, mutation_rate, max_depth, current_depth + 1)

    return node


def crossover(parent1, parent2, max_depth=8):
    subtree1 = select_random_subtree(parent1)
    subtree2 = select_random_subtree(parent2)

    if tree_depth(subtree1) + tree_depth(subtree2) > max_depth:
        return parent1, parent2

    if not is_compatible(subtree1, subtree2):
        return parent1, parent2

    replace_subtree(parent1, subtree1, subtree2)
    replace_subtree(parent2, subtree2, subtree1)

    return parent1, parent2


def select_random_subtree(tree):
    all_subtrees = get_all_subtrees(tree)
    return random.choice(all_subtrees)


def get_all_subtrees(node):
    subtrees = [node]
    for child in node.children:
        subtrees.extend(get_all_subtrees(child))
    return subtrees


def replace_subtree(tree, subtree_to_replace, new_subtree):
    if tree == subtree_to_replace:
        copy_attributes(new_subtree, tree)
    else:
        for i, child in enumerate(tree.children):
            if child == subtree_to_replace:
                tree.children[i] = new_subtree
                return
            replace_subtree(child, subtree_to_replace, new_subtree)


def copy_attributes(source_node, target_node):
    target_node.value = source_node.value
    target_node.children = source_node.children


def modified_tournament_selection_and_crossover(
    population, points, mutation_rate, fitnesses, k
):
    population_size = len(population)

    best_indices = sorted(range(population_size), key=lambda i: fitnesses[i])[:2]
    best_individuals = [population[i] for i in best_indices]

    new_population = [None] * population_size
    new_population[0:2] = best_individuals

    for i in range(2, population_size):
        tournament_indices = []
        j = 3
        while j > 0:
            indice = random.randint(0, population_size - 1)
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

        child1, child2 = crossover(parent1, parent2)

        child1 = mutate_tree(child1, mutation_rate)
        child2 = mutate_tree(child2, mutation_rate)

        chosen_child = random.choice([child1, child2])
        new_population[i] = chosen_child

    new_route = [tsp_solver(points, k, individual) for individual in new_population]

    new_fitnesses = []

    for ja in new_route:
        new_fitnesses.append(calculate_fitness(ja, points))
    return new_population, new_fitnesses

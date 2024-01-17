import random
from tsp_context import *


operators = {
    "+": 2,
    "-": 2,
    "*": 2,
    "/": 2,
}

terminals = [
    "distance",
    "density",
    "average",
]


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def __repr__(self):
        return f"{self.value}: {[child.value for child in self.children]}"

    def evaluate(self, context):
        if self.value in operators:
            operands = [child.evaluate(context) for child in self.children]
            return self.apply_operator(operands)
        else:
            return self.apply_function(self.value, context)

    def apply_operator(self, operands):
        op = self.value
        if op == "+":
            return operands[0] + operands[1]
        if op == "-":
            return operands[0] - operands[1]
        if op == "*":
            return operands[0] * operands[1]
        if op == "/":
            return operands[0] / operands[1] if operands[1] != 0 else float("inf")
        raise ValueError(f"Unknown operator: {op}")

    def apply_function(self, func, context):
        if func == "distance":
            return context["distance"]
        if func == "density":
            return context["density"]
        if func == "average":
            return context["average"]
        raise ValueError(f"Unknown function: {func}")


def random_operator():
    op = random.choice(list(operators.keys()))
    arity = operators[op]
    return op, arity


def random_terminal():
    return random.choice(terminals)


def random_chance(prob=0.2):
    return random.random() < prob


def create_random_tree(max_depth, depth=0):
    if depth == max_depth or random_chance():
        return Node(random_terminal())
    else:
        op, arity = random_operator()
        children = [create_random_tree(max_depth, depth + 1) for _ in range(arity)]
        return Node(op, children)


def inorder_traversal(node):
    if node:
        if len(node.children) == 2:
            print("(", end="")
            inorder_traversal(node.children[0])

            print(f" {node.value} ", end="")

            inorder_traversal(node.children[1])
            print(")", end="")
        else:
            print(node.value, end="")


def create_context(current_city, unvisited_cities, distances, densities):
    context = {
        "distance": tsp_nearest_city_distance(
            current_city, unvisited_cities, distances
        ),
        "density": tsp_current_city_density(current_city, densities),
        "average": tsp_calculate_average_distance(
            current_city, unvisited_cities, distances
        ),
    }
    return context


def choose_next_city(current_city, unvisited_cities, distances, densities, tree):
    best_city = None
    best_score = None
    for city in unvisited_cities:
        context = create_context(city, unvisited_cities, distances, densities)
        score = tree.evaluate(context)
        if best_score == None or score > best_score:
            best_city = city
            best_score = score
    return best_city


def tsp_solver(points, k, tree):
    num_cities = len(points)
    current_city = 0
    unvisited_cities = set(range(num_cities))

    if current_city in unvisited_cities:
        unvisited_cities.remove(current_city)

    route = [current_city]

    distances = [[tsp_calculate_distance(p1, p2) for p2 in points] for p1 in points]
    densities = tsp_city_density(points, k)

    while unvisited_cities:
        next_city = choose_next_city(
            current_city, unvisited_cities, distances, densities, tree
        )
        route.append(next_city)
        unvisited_cities.remove(next_city)
        current_city = next_city

    route.append(0)
    return route

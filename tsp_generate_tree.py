import random
from tsp_context import *


function_set = ["+", "-", "*", "/"]
terminal_set = [
    "radius",
    "nearest_distance",
    "distance",
    "random_average",
    "average",
    "density",
]


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    __repr__ = __str__ = lambda self: str(self.value)

    def evaluate(self, context):
        if self.value in function_set:
            return self.apply_operator(
                [self.left.evaluate(context), self.right.evaluate(context)]
            )
        elif self.value in terminal_set:
            return self.apply_function(self.value, context)

    def apply_operator(self, operands):
        op = self.value
        if op == "+":
            # print(op, operands)
            # print(operands[0] + operands[1])
            return operands[0] + operands[1]
        if op == "-":
            # print(op, operands)
            # print(operands[0] - operands[1])
            return operands[0] - operands[1]
        if op == "*":
            # print(op, operands)
            # print(operands[0] * operands[1])
            return operands[0] * operands[1]
        if op == "/":
            # print(op, operands)
            # print(operands[0] / operands[1])
            return operands[0] / operands[1] if operands[1] != 0 else float("inf")
        raise ValueError(f"Unknown operator: {op}")

    def apply_function(self, func, context):
        if func == "nearest_distance":
            return context["nearest_distance"]
        if func == "density":
            return context["density"]
        if func == "average":
            return context["average"]
        if func == "radius":
            return context["radius"]
        if func == "distance":
            return context["distance"]
        if func == "random_average":
            return context["random_average"]
        raise ValueError(f"Unknown function: {func}")


# OK
def create_context(
    current_city, second_city, unvisited_cities, distances, densities, points
):
    context = {
        "nearest_distance": tsp_nearest_city_distance(
            current_city, second_city, distances, unvisited_cities
        ),
        "density": tsp_current_city_density(current_city, densities),
        "average": tsp_calculate_average_distance(
            current_city, unvisited_cities, distances
        ),
        "radius": tsp_points_within_radius(current_city, points, 20),
        "distance": tsp_calculate_distance_from_origin(
            current_city, second_city, distances
        ),
        "random_average": random_average_distance(
            current_city, unvisited_cities, distances
        ),
    }
    return context


# OK
def choose_next_city(
    current_city, unvisited_cities, distances, densities, tree, points
):
    best_city = None
    best_score = None
    for city in unvisited_cities:
        context = create_context(
            current_city, city, unvisited_cities, distances, densities, points
        )
        score = tree.evaluate(context)
        if best_score == None or score > best_score:
            best_city = city
            best_score = score
    return best_city


# OK
def tsp_route_finder(points, k, tree):
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
            current_city, unvisited_cities, distances, densities, tree, points
        )
        route.append(next_city)
        unvisited_cities.remove(next_city)
        current_city = next_city

    route.append(0)
    return route


# OK
def random_expression_tree(depth, function_set, terminal_set):
    if depth == 0 or random.random() < 0.3:
        return Node(random.choice(terminal_set))
    else:
        node = Node(random.choice(function_set))
        node.left = random_expression_tree(depth - 1, function_set, terminal_set)
        node.right = random_expression_tree(depth - 1, function_set, terminal_set)
        return node


# OK
def inorder_traversal(root):
    if root is not None:
        if root.left is not None and root.right is not None:
            print("(", end="")

        inorder_traversal(root.left)
        print(root.value, end="")
        inorder_traversal(root.right)

        if root.left is not None and root.right is not None:
            print(")", end="")

import math
import random


def tsp_points_within_radius(current_point, points, radius):
    count = 0

    for point in points:
        distance = tsp_calculate_distance(points[current_point], point)

        if distance <= radius:
            count += 1 / len(points)
    return count


# OK
def tsp_calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# OK
def tsp_calculate_distance_from_origin(current_city, second_city, distances):
    return 1 / distances[current_city][second_city]


def tsp_nearest_city_distance(current_city, second_city, distances, unvisited_cities):
    filtered_cities = [city for city in unvisited_cities if city != current_city]

    if not filtered_cities:
        return 1

    nearest_distance = min(distances[current_city][city] for city in filtered_cities)

    return 1 / nearest_distance


# OK
def tsp_city_density(points, k):
    densities = []
    for i, point in enumerate(points):
        distances = sorted(
            [
                tsp_calculate_distance(point, other)
                for j, other in enumerate(points)
                if i != j
            ]
        )

        avg_distance = sum(distances[:k]) / k
        density = 1 / avg_distance if avg_distance != 0 else float("inf")

        densities.append(density)

    return densities


# OK
def tsp_current_city_density(current_city, densities):
    return densities[current_city]


# OK
def tsp_calculate_average_distance(city_index, unvisited_cities, distances):
    if not unvisited_cities:
        return float("inf")

    total_distance = sum(
        distances[city_index][other_city]
        for other_city in unvisited_cities
        if other_city != city_index
    )
    average_distance = total_distance / len(unvisited_cities)
    return 1 / average_distance


def random_average_distance(city_index, unvisited_cities, distances):
    num_unvisited = len(unvisited_cities)

    if num_unvisited >= 3:
        selected_cities = random.sample(list(unvisited_cities), 3)
    elif num_unvisited == 2:
        selected_cities = list(unvisited_cities)
    elif num_unvisited == 1:
        selected_cities = [next(iter(unvisited_cities))]
    else:
        return float("inf")

    total_distance = sum(
        distances[city_index][other_city] for other_city in selected_cities
    )
    average_distance = total_distance / len(selected_cities)

    return average_distance

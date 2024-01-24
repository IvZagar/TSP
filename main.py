from tsp_create import *
from tsp_context import *
from tsp_generate_tree import *
from tsp_genetic_alghoritm import *
import matplotlib.pyplot as plt

folder_path = r"C:\Users\ivanz\OneDrive\Desktop\TSP\tsp_points"
file_path = r"C:\Users\ivanz\OneDrive\Desktop\TSP\tsp_points\points_2.txt"
x_range = (1, 99)
y_range = (1, 99)
num_points = 50
k = 3

# tsp_save_points(folder_path, tsp_generate_random_points(num_points, x_range, y_range))


def tsp_plot_route(ax, points, tour, color="b", alpha=1.0, linewidth=1.0):
    x, y = zip(*[points[i] for i in tour])
    ax.plot(
        x,
        y,
        marker="o",
        linestyle="-",
        markersize=3,
        color=color,
        alpha=alpha,
        linewidth=linewidth,
    )

    ax.plot(x[0], y[0], marker="o", markersize=5, color="black")
    ax.text(
        x[0],
        y[0],
        "You are here",
        fontsize=10,
        color="black",
        verticalalignment="bottom",
    )

    ax.set_title("TSP Tour")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.grid(False)


def main():
    plt.ion()
    fig, ax = plt.subplots()

    population_size = 10
    generations = 1000
    mutation_rate = 0.15
    points = tsp_read_points(file_path)
    population = []
    while population_size:
        tree = random_expression_tree(3, function_set, terminal_set)
        route = tsp_route_finder(points, k, tree)
        if tree not in [p[1] for p in population] and route not in [
            p[0] for p in population
        ]:
            population.append((route, tree))
            population_size -= 1

    fitness_per_generation = []
    best_tour = None
    best_fitness = float("inf")

    all_routes = []
    for gen in range(generations):
        fitnesses = [calculate_fitness(tree[0], points) for tree in population]
        print(fitnesses)
        population, z = modified_tournament_selection_and_crossover(
            population,
            points,
            mutation_rate,
            fitnesses,
            k,
        )

        current_best_fitness = min(z)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_tour = population[z.index(best_fitness)][0]

        print(f"Generation {gen + 1}: Best Fitness = {best_fitness}")
        fitness_per_generation.append(best_fitness)

        ax.clear()
        for route in all_routes:
            tsp_plot_route(ax, points, route, color="grey", alpha=0.1, linewidth=0.2)

        tsp_plot_route(ax, points, best_tour, color="#006400", alpha=1.0, linewidth=1.5)
        ax.set_title(f"Generation {gen + 1}: Best Fitness = {best_fitness}")

        plt.pause(0.01)

        all_routes.append(best_tour)
    print(f"Route = {best_tour}")
    print(f"Function = {population[0][1]}")

    ax.clear()
    plt.bar(range(1, generations + 1), fitness_per_generation, color="green")
    plt.title("Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()

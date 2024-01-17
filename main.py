from tsp_create import *
from tsp_context import *
from tsp_generate_tree import *
from tsp_genetic_alghoritm import *
import matplotlib.pyplot as plt


folder_path = r"C:\Users\ivanz\OneDrive\Desktop\PROJEKT R\tsp_points"
file_path = r"C:\Users\ivanz\OneDrive\Desktop\PROJEKT R\tsp_points\points_2.txt"
x_range = (1, 99)
y_range = (1, 99)
num_points = 50
k = 3

# tsp_save_points(folder_path, tsp_generate_random_points(num_points, x_range, y_range))


def main():
    population_size = 10
    generations = 100
    mutation_rate = 0.05
    points = tsp_read_points(file_path)

    population = [create_random_tree(max_depth=3) for _ in range(population_size)]

    average_fitness_per_generation = []

    for gen in range(generations):
        fitnesses = [
            calculate_fitness(tsp_solver(points, k, tree), points)
            for tree in population
        ]
        population, z = modified_tournament_selection_and_crossover(
            population, points, mutation_rate, fitnesses, k
        )

        best_fitness = min(fitnesses)
        print(f"Generation {gen + 1}: Best Fitness = {best_fitness}")
        average_fitness_per_generation.append(best_fitness)

    plt.bar(range(1, generations + 1), average_fitness_per_generation, color="blue")
    plt.title("Average Fitness Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    plt.show()


if __name__ == "__main__":
    main()

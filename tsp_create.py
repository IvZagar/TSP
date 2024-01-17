import random
import os


def tsp_generate_random_points(num_points, x_range, y_range):
    points = []
    for _ in range(num_points):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        points.append((x, y))
    return points


def tsp_read_points(file_path):
    points = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                x_str, y_str = line.strip().replace("(", "").replace(")", "").split(",")
                point = (float(x_str), float(y_str))
                points.append(point)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except ValueError as e:
        print(f"Error reading the file {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return points


def tsp_save_points(folder_path, data):
    try:
        os.makedirs(folder_path, exist_ok=True)

        file_index = len(
            [
                f
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".py")
            ]
        )

        new_file_name = f"points_{file_index}.txt"
        new_file_path = os.path.join(folder_path, new_file_name)

        while os.path.exists(new_file_path):
            file_index += 1
            new_file_name = f"points_{file_index}.txt"
            new_file_path = os.path.join(folder_path, new_file_name)

        with open(new_file_path, "w") as new_file:
            for i in range(len(data)):
                if i < len(data) - 1:
                    new_file.write(str(data[i]) + "\n")
                else:
                    new_file.write(str(data[i]))

        print(f"Data successfully saved to {new_file_path}")

    except Exception as e:
        print(f"ERROR - Unable to save the file: {e}")

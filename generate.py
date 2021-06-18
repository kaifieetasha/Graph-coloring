import random


class Vertex:
    def __init__(self, index):
        self.index = index
        self.neighbours = []


def generate_neighbours(current_index, max_index, max_neighbours):
    neighbours = []
    while len(neighbours) < 1:
        for n in range(1, random.randint(1, max_neighbours)):
            new_neighbour = random.randint(0, max_index)
            if new_neighbour != current_index:
                neighbours.append(new_neighbour)
        neighbours = list(set(neighbours))
    return neighbours


def generate_graph(vertices_number, output_file):
    if vertices_number < 4:
        exit(1)

    vertices = [Vertex(i) for i in range(vertices_number)]
    for v in vertices:
        v.neighbours += generate_neighbours(v.index, vertices_number-1, int(vertices_number/2))
        for n in v.neighbours:
            if v.index not in vertices[n].neighbours:
                vertices[n].neighbours.append(v.index)

    with open(output_file, "w") as file:
        for v in vertices:
            line = str(v.index) + " "
            for n in v.neighbours:
                line += str(n) + " "
            line += "\n"
            file.write(line)


generate_graph(4, "dane3.txt")

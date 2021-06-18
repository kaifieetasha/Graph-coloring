class Vertex:

    def __init__(self):
        self.neighbours = []
        self.color = 1

    def __lt__(self, other):
        return len(self.neighbours) < len(other.neighbours)

def goal_for_vertex(vertex):
    for neighbour in vertex.neighbours:
        if neighbour.color == vertex.color:
            return False
    return True


def goal(vertices):
    for vertex in vertices:
        if not goal_for_vertex(vertex):
            return False
    return True


def get_from_file(file_name):
    output = []

    with open(file_name, "r") as file:
        for line in file:
            output.append(Vertex())

    with open(file_name, "r") as file:
        for line in file:
            tokens = line.split()
            for token in tokens[1:]:
                output[int(tokens[0])].neighbours.append(output[int(token)])

    return output


def main():
    graph = get_from_file("dane3.txt")
    graph.sort()

    for vertex in graph:
        while not goal_for_vertex(vertex):
            vertex.color += 1

    count_color = 1
    for vertex in graph:
        if vertex.color > count_color:
            count_color = vertex.color

    if goal(graph):
        print("cel spełniony, wymagana liczba kolorów to", count_color)
        exit(0)
    else:
        print("cel nie spełniony")
        exit(1)


main()

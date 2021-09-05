from sys import argv
from time import sleep
from math import exp
from random import randint, random


class Point:
    def __init__(self, color, neighbours):
        self.color = color
        self.neighbours = neighbours

    def copy(self):
        return Point(self.color, self.neighbours)


def describePoints(points):
    for i in range(0, len(points)):
        print('\tPunkt', i + 1, 'kolor:', points[i].color, ', Sąsiedzi:', points[i].neighbours)
    print('\tOcena rozwiązania:', "{:.2f}".format(goal(points)))


def randomSolution(points):
    for p in points:
        p.color = randint(0, len(points) - 1)


def nextSolution(points):
    def incrementColor(index):
        if points[index].color < len(points) - 1:
            points[index].color += 1
        else:
            points[index].color = 0
            incrementColor(index - 1)

    if [p.color for p in points] == [i for i in range(0, len(points))]:
        return 0
    else:
        incrementColor(len(points) - 1)
        return 1


def pointsFromFile(file):
    points = []
    with open(file, "r") as file:
        for line in file:
            numbers = line.replace("\n", "").split(" ")
            points.append(Point(0, [int(n) for n in numbers[1:]]))
    return points


def goal(points):
    result = 0
    for p in points:
        for n in p.neighbours:
            if p.color == points[n - 1].color:
                result = result - 1
    if result < 0:
        return result
    return (1 / len(set([p.color for p in points]))) * 2


def fitness(goal):
    if goal < 0:
        return -(1 / goal) / 2
    return goal


def generateGraph(n):
    points = [Point(0, []) for i in range(0, n)]
    i = 0
    for p in points:
        i += 1
        neighboursCount = randint(1, int(len(points) / 2))
        while len(p.neighbours) < neighboursCount:
            p.neighbours.append(randint(1, n))
            p.neighbours = list(filter(lambda a: a != i, p.neighbours))
            p.neighbours = list(set(p.neighbours))
        for ne in p.neighbours:
            points[ne - 1].neighbours.append(i)
    for p in points:
        p.neighbours = list(set(p.neighbours))
    return points


def newPoints(points, chanceToGenerateNewColor):
    pointsCopy = [p.copy() for p in points]
    index = randint(0, len(pointsCopy) - 1)
    decision = randint(0, chanceToGenerateNewColor)
    if decision == 0:
        maxColor = max([p.color for p in pointsCopy])
        pointsCopy[index].color = maxColor + 1
    else:
        otherIndex = index
        while index == otherIndex:
            otherIndex = randint(0, len(pointsCopy) - 1)
        pointsCopy[index].color = pointsCopy[otherIndex].color
    return pointsCopy


def wspinaczka(points, variant='random'):
    if variant == 'random':
        print('Wspinaczka przypadkowa\n')
        while goal(points) < 0:
            new_points = newPoints(points, 200000)
            if goal(new_points) > goal(points):
                points = new_points
        # po kolei w celu znalezienia najlepszego rozwiązania
    elif variant == 'determine':
        print('Wspinaczka deterministyczna\n')
        new_points = [p.copy() for p in points]
        while nextSolution(new_points) == 1:
            if goal(new_points) > goal(points):
                points = new_points
                new_points = [p.copy() for p in points]
    return points


def wyżarzanie(points):
    iterations = 10000
    temperature = 1
    while (temperature > 0):
        for i in range(0, iterations):
            new_points = newPoints(points, 100000)
            costDifference = (goal(new_points) - goal(points)) * -1
            rho = exp(-costDifference / temperature)
            if random() <= rho:
                points = new_points
        print('Temperatura :', "{:.2f}".format(temperature), 'Ocena :', "{:.2f}".format(fitness(goal(points))))
        temperature -= 0.005
    return points


def demo():
    n = 4
    print(f"Generuję graf z {n} punktami")
    sleep(2)
    points = generateGraph(n)
    describePoints(points)
    sleep(2)
    print("Deterministyczne wygenerowanie 10 kolejnych rozwiązań:")
    sleep(2)
    for i in range(0, 10):
        nextSolution(points)
        describePoints(points)
        sleep(2)
    print("Generowanie losowego rozwiązania:")
    sleep(2)
    randomSolution(points)
    describePoints(points)


if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == 'demo':
            demo()
            exit(0)
        else:
            points = pointsFromFile(argv[1])
    else:
        points = generateGraph(8)

    print('Przed optymalizacją: ')
    describePoints(points)

    # print('\nRozpoczynam algorytm wspinaczkowy')
    # points = wspinaczka(points, 'random')

    print('\nRozpoczynam algorytm symulowanego wyżarzanie')
    points = wyżarzanie(points)

    print('Po optymalizacji:')
    describePoints(points)

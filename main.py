#!/usr/bin/python 3
# coding: utf-8

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        #                                                                   #
        #                   MESTRADO EM CIENCIAS DA COMPUTACAO              #
        #           DISCIPLINA DE COMPUTACAO INSPIRADA PELA NATUREZA        #
        #                   Thiago Giroto Milani    -   01/2017             #
        #                                                                   #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#Biblioteca
import math

from aco import ACO, Graph
from plot import plot


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    cities = []
    points = []
    # Le o arquivo do dataset dentro da pasta data.
    with open('./data/berlin52.tsp.txt') as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=float(city[0]), x=float(city[1]), y=float(city[2])))
            points.append((float(city[1]), float(city[2])))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    # Chama o ACO passando os parametros
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)

if __name__ == '__main__':
    main()

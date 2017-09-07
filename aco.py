#!/usr/bin/python 3
# coding: utf-8

		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
		#																	#
		#					MESTRADO EM CIENCIAS DA COMPUTACAO				#
		#			DISCIPLINA DE COMPUTACAO INSPIRADA PELA NATUREZA		#
		#					Thiago Giroto Milani	-	01/2017				#
		#																	#
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#Biblioteca

import random


class Graph(object):
    def __init__(self, cost_matrix: list, rank: int):
        """
        :parametro cost_matrix:
        :parametro rank: rank de curso de matriz
        """
        self.matrix = cost_matrix
        self.rank = rank
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, rho: float, q: int, strategy: int):
        """
        :parametro ant_count:
        :parametro generations:
        :parametro alpha: importancia relativa do feromonio
        :parametro beta: importancia relativa da informacao heuristica
        :parametro rho: coeficiente residual de feromonio 
        :parametro q: intensidade do feromonio
        :parametro da estrategia: estrategia de atualizacao de feromonio. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy

    def _update_pheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph: Graph):
        """
        :parametro do grafo:
        """
        best_cost = float('inf')
        best_solution = []
        for gen in range(self.generations):
            ants = [_Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                for i in range(graph.rank - 1):
                    ant._select_next()
                ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tabu
                # atualiza feromonio
                ant._update_pheromone_delta()
            self._update_pheromone(graph, ants)
######
            print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # Lista de tabu
        self.pheromone_delta = []  # Aumento local de feromonio
        self.allowed = [i for i in range(graph.rank)]  # nos que sao permitidos para a proxima selecao
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in
                    range(graph.rank)]  # Informacao heuristica
        start = random.randint(0, graph.rank - 1)  # Inicia de um no aleatorio
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _select_next(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta
        probabilities = [0 for i in range(self.graph.rank)]  # probabilidades de se mudar para um no na próxima etapa
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)  # Testa se a lista i tem permicao
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass
        # selecionar o proximo no pela probabilidade de roleta
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colony.update_strategy == 1:  # sistema de qualidade 
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # sistema de densidade
                self.pheromone_delta[i][j] = self.colony.Q / self.graph.matrix[i][j]
            else:  # sistema de ciclo
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost

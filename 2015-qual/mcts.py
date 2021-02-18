import random as rd
from copy import deepcopy
from node import Node
from montecarlo import MonteCarlo

from solution import Solution


def mcts_find_best_child(sol, simulations_nb=10):  # TODO ajouter parametres exploration pour cloture
	def child_finder(node):
		for move in node.state.get_possible_moves():
			child = Node(deepcopy(node.state))
			child.state.apply(move)
			node.add_child(child)

	def node_evaluator(node, root):
		return node.state.score

	montecarlo = MonteCarlo(sol)
	montecarlo.child_finder = child_finder
	montecarlo.node_evaluator = node_evaluator

	montecarlo.simulate(simulations_nb)

	return montecarlo.make_choice()


def mcts_explore(sol, simulations_by_move, moves_nb, eps=1/4):
	def child_finder(node):
		for move in node.state.get_possible_moves():
			child = Node(deepcopy(node.state))
			child.state.apply(move)
			node.add_child(child)

	def node_evaluator(node, root):
		return node.state.score

	montecarlo = MonteCarlo(sol)
	montecarlo.child_finder = child_finder
	montecarlo.node_evaluator = node_evaluator

	for i in range(moves_nb):
		print(f'try nb {i}')

		montecarlo.simulate(simulations_by_move)
		print('height :', montecarlo.get_tree_height())
		print('nb of children :', len(sol.children))

		sub_sol = montecarlo.make_choice()

		if sub_sol.state.score > sol.state.score or rd.random() < eps:
			sol = sub_sol
			print('new best score :', sol.state.score)
		
		state = sol.state
		children = sol.children
		wv = sol.win_value
		visits = sol.visits

		sol = Node(state)
		sol.children = children
		sol.expanded = True
		sol.win_value = wv
		sol.visits = visits

		montecarlo = MonteCarlo(sol)
		montecarlo.child_finder = child_finder
		montecarlo.node_evaluator = node_evaluator
	
	return sol
import random

class MonteCarlo:

	def __init__(self, root_node):
		self.root_node = root_node
		self.child_finder = None
		self.node_evaluator = lambda child, montecarlo: None
	
	def print_tree(self):
		self.root_node.print_recursive()
	
	def get_tree_height(self):
		return self.root_node.compute_sub_height()

	def make_choice(self):
		best_children = []
		most_visits = float('-inf')

		for child in self.root_node.children:
			# print('child visits', child.visits)
			if child.visits >= most_visits:
				most_visits = child.visits
				best_children.append(child)

		if not best_children:
			raise Exception('Root node has no child')

		return random.choice(best_children)

	def make_exploratory_choice(self):
		children_visits = map(lambda child: child.visits, self.root_node.children)
		children_visit_probabilities = [visit / self.root_node.visits for visit in children_visits]
		random_probability = random.uniform(0, 1)
		probabilities_already_counted = 0.
		# TODO choices
		for i, probability in enumerate(children_visit_probabilities):
			if probabilities_already_counted + probability >= random_probability:
				return self.root_node.children[i]

			probabilities_already_counted += probability

	def simulate(self, expansion_count=1):
		for _ in range(expansion_count):
			# print('entering one expansion')

			current_node = self.root_node

			while current_node.expanded:
				# print('following path')
				current_node = current_node.get_preferred_child(self.root_node)

			self.expand(current_node)
			# print('finished one simulation')

	def expand(self, node):
		self.child_finder(node)

		# print('expanding node', (self))
		# print('len of current expanded node', len(node.children))
		for child in node.children:
			
			child_win_value = self.node_evaluator(child, self)
			# print('child win value', child_win_value)

			if child_win_value != None:
				child.update_win_value(child_win_value)

		if len(node.children):
			# print('SETTING AS EXPANDED')
			node.expanded = True
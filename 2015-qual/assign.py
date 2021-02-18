from ortools.linear_solver import pywraplp


def create_data_model(bin_capacities, weights, values):
    """Create the data for the example."""
    data = {}
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    data['bins'] = list(range(len(bin_capacities)))
    data['bin_capacities'] = bin_capacities
    return data


def solve_multi_knapsack(bin_capacities, weights, values):
    data = create_data_model(bin_capacities, weights, values)

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_value = objective.Value()
        total_weight = 0
        bins_content = []
        for j in data['bins']:
            bin_weight = 0
            bin_value = 0
            bin_content = []
            for i in data['items']:
                if x[i, j].solution_value() > 0:
                    bin_content.append(i)
                    bin_weight += data['weights'][i]
            total_weight += bin_weight
            bins_content.append(bin_content)
        return total_value, total_weight, bins_content
    raise Exception('Problem has no solution')
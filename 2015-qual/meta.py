def compute_max_possible_score(d):
    capacities = [server['capacity'] for server in d['servers']]
    capacities.sort()
    total_capacity = sum(capacities)
    return (total_capacity - sum(capacities[:d['pools_nb']])) / d['pools_nb']
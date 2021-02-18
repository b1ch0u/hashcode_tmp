from parser import Solution, Data, Target, File
from copy import deepcopy

from utils import compute_dependencies


def compute_all_dependencies(d, target):
    data = deepcopy(d)
    dependencies = data.files[target].dependencies
    dependencies_list = []
    while dependencies:
        file_to_compile = data.files[dependencies.pop(0)]
        dependencies.extend(file_to_compile.dependencies)
        dependencies_list.append(file_to_compile.name)
    return dependencies_list


def compute_time_to_compile_target_file(data, target):
    time_to_compile = 0
    dependencies = compute_all_dependencies(data, target)
    for dependence in dependencies:
        time_to_compile += data.files[dependence].compile_time
    return time_to_compile


def simple_solution(data):
    sol = Solution(0, [])
    servers_step = []
    for i in range(data.servers_nb):
        servers_step.append([])
    target_sorted = []
    target_list = []
    target_files = data.targets
    for t in target_files.values():
        target_list.append(t.name)
    target_time_to_compile = []
    target_score = []
    for target in target_list:
        time_to_compile = compute_time_to_compile_target_file(data, target)
        target_time_to_compile.append(time_to_compile)
        if time_to_compile != 0:
            target_score.append(data.targets[target].points / time_to_compile)
        else:
            target_score.append(0)
    
    while target_score:
        index = 0
        for i in range(len(target_score)):
            if target_score[i] > target_score[index]:
                index = i
        target_sorted.append(target_list.pop(index))
        target_score.pop(index)
    
    for i in range(len(target_sorted)):
        all_d = compute_dependencies(data.files[target_sorted[i]])
        all_d = all_d[::-1]
        all_d.append([target_sorted[i]])
        for level_list in all_d:
            for file in level_list:
                if file not in servers_step[i % data.servers_nb]:
                    servers_step[i % data.servers_nb].append(file)
    
    for i in range(len(servers_step)):
        for step in servers_step[i]:
            sol.steps.append((step,i))
            sol.steps_nb += 1
    
    return sol
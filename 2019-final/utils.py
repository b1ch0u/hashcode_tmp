from copy import deepcopy

def total_goalpts(d):
    sum=0
    for t in d.targets :
        sum+=t.points
    return sum

# def compute_dependencies(d, file):
#     data = deepcopy(d)
#     all_dependencies = []
#     dependencies = data.files[file].dependencies
#     d_level = []
#     for d in dependencies:
#         d_level.append([d,0])
#     while dependencies:
#         next_level_dependencies = []
#         for d in dependencies:
#             next_level_dependencies.extend(data.files[d].dependencies)
#         if next_level_dependencies:
#             for i in range(len(d_level)):
#                 d_level[i][1] += 1
#             for d in dependencies:
#                 d_level.append([d,0])
#         dependencies = next_level_dependencies
#     lvl = 0
#     while d_level:
#         level_dependencies = []
#         item_to_remove = []
#         for i in range(len(d_level)):
#             if d_level[i][1] == lvl:
#                 level_dependencies.append(d_level[i][0])
#         index = 0
#         for d in d_level:
#             if d[1] == lvl:
#                 d_level.pop(index)
#             else:
#                 index += 1
#         all_dependencies.append(level_dependencies)
#         lvl += 1
#     return all_dependencies

def compute_dependencies(file, levels=None, depth=0):
    if levels is None:
        levels = []
    if len(levels) <= depth and file.file_dependencies:
        levels.append(set())
    if file.file_dependencies:
        levels[depth] |= set(f.name for f in file.file_dependencies)
        for dep in file.file_dependencies:
            compute_dependencies(dep, levels, depth + 1)
    return levels
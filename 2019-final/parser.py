from os import O_NOATIME
from dataclasses import dataclass
from collections import deque

from memoize import Memorize


@dataclass
class File:
    name: str
    compile_time: int
    replicate_time: int
    dependencies: list

    file_dependencies: list = None
    min_time: int = None
    potential: int = 0
    heuristic: float = None

    def set_min_time(self):
        if self.min_time is None:
            for file in self.file_dependencies:
                file.set_min_time()
            dep_min_time = 0 if not self.file_dependencies \
                            else max(f.min_time for f in self.file_dependencies) 
            self.min_time = self.compile_time + dep_min_time  # TODO tenir compte de la latence
    
    def propagate_potential(self):
        for f in self.file_dependencies:
            f.potential += self.potential
            f.propagate_potential()



@dataclass
class Target:
    name: str
    deadline: int
    points: int


@dataclass
class Data:
    files_nb: int
    targets_nb: int
    servers_nb: int
    files: dict
    targets: dict


@dataclass
class Solution:
    steps_nb: int
    steps: list


@Memorize
def parse(filename):
    with open(filename) as f:
        lines = deque(line for line in f)

    files_nb, targets_nb, servers_nb = map(int, lines.popleft().rstrip('\n').split(' '))

    files = {}
    for i in range(files_nb):
        name, compile_time, replicate_time = lines.popleft().rstrip('\n').split(' ')
        _, *dependencies = lines.popleft().rstrip('\n').split(' ')
        files[name] = File(name, int(compile_time), int(replicate_time), dependencies)
    
    targets = {}
    for _ in range(targets_nb):
        name, deadline, points = lines.popleft().rstrip('\n').split(' ')
        targets[name] = Target(name, int(deadline), int(points))
    
    
    for file in files.values():
        file.file_dependencies = [files[name] for name in file.dependencies]
    
    for target in targets.values():
        files[target.name].potential = target.points
        files[target.name].propagate_potential()

    for file in files.values():
        file.set_min_time()

    for file in files.values():
        file.heuristic = file.potential / file.min_time

    return Data(files_nb, targets_nb, servers_nb, files, targets)
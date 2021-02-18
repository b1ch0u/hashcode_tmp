from memoize import Memorize

from utils import Data, Photo


@Memorize
def parse(filename):
    with open(filename) as f:
        lines = [line for line in f]

    N = int(lines.pop(0))

    photos = []
    for id in range(N):
        line = lines.pop(0).rstrip('\n').split(' ')
        orientation = line[0]
        tags = frozenset(line[2:])
        photos.append(Photo(id, orientation, tags))

    return Data(N, photos)
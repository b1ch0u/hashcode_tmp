import random

from utils import compute_interest, Slide, Solution

from memoize import Memorize

from matching import compute_matching_max, total_affinity

from copy import deepcopy


# TODO memoize by filename
def naive_vertical_slides(data, group_size=100):
    slides = []
    photos = deepcopy(data.photos)
    random.shuffle(photos)

    for photo in photos:
        if photo.orientation == "H":
            slides.append(Slide.from_H_photo(photo))
    photos_V = [photo for photo in photos if photo.orientation == 'V']
    # while len(photos_V) > 1:
    #     slides.append(Slide("V", photos_V.pop(0), photos_V.pop(0), photo.tags))
    while photos_V:
        sublist = photos_V[:group_size]
        list_id = compute_matching_max(sublist, total_affinity)
        for p1, p2 in list_id:
            tags = photos[p1].tags | photos[p2].tags
            slides.append(Slide("V", p1, p2, tags))
        if len(photos_V) % 200 == 0:
            print(f'matching ... remaining {int(len(photos_V) / group_size)}')
        if len(sublist) == group_size:
            photos_V = photos_V[group_size:]
        else:
            break
    return slides
    


def greedy_solution(slides, groups_size=1000):
    sol = Solution([])
    random.shuffle(slides)
    slides = deque(slides)
    sol.add_slide(slides.pop())

    while slides:
        if len(slides) % 100 == 0:
            print(f'remaining {len(slides)}\tcurrent score: {sol.score}')

        best_score = -1
        for i, slide in enumerate(slides):
            if i > groups_size:
                break
            interest = compute_interest(sol.slides[-1].tags, slide.tags)
            if interest > best_score:
                best_score = interest
                best_slide_id = i

        slides.rotate(-best_slide_id)
        sol.add_slide(slides.popleft())        
    
    return sol


from collections import deque


def better_greedy(slides):
    sol = Solution([])
    random.shuffle(slides)
    d = deque(slides)
    current_slide = d.popleft()
    sol.add_slide(current_slide)
    while d:
        if len(d) % 1000 == 0:
            print('remaining', len(d), '\tcurrent score :', sol.score)
        for i, slide in enumerate(d):
            if compute_interest(current_slide.tags, slide.tags):
                d.rotate(-i)
                current_slide = d.popleft()
                sol.add_slide(current_slide)
                break
        else:
            current_slide = d.popleft()
            sol.add_slide(current_slide)
    return sol

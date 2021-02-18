from copy import deepcopy

from utils import *


def extract_subgroup(slides, max_len=100):
    tags = slides[0].tags
    return [slide for slide in slides
            if slide.tags & tags]


def form_solution_by_subgroups(slides):
    photos = deepcopy(slides)
    res = Solution()
    while photos:
        group = extract_subgroup(slides)

        sol = create_tsp_solution(group)

        path = sol[0]
        # slides = []
        s = Solution([])
        for p_id in path:
            p = data.photos[p_id]
            # slides.append()
            s.add_slide(Slide.from_H_photo(p))
        
        print('score :', s.score)

        print(sol)
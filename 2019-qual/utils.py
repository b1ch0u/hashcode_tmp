from dataclasses import dataclass


@dataclass
class Data:
    N: int
    photos: list


@dataclass
class Photo:
    id: int
    orientation: str
    tags: frozenset


@dataclass
class Slide:
    orientation: str
    left_id: int
    right_id: int
    tags: frozenset

    @staticmethod
    def from_H_photo(photo):
        return Slide(photo.orientation, photo.id, photo.id, photo.tags)
    
    def to_str(self):
        if self.orientation == 'H':
            return str(self.left_id)
        return str(self.left_id) + ', ' + str(self.right_id)


@dataclass
class Solution:
    slides: list
    score: int = 0

    def add_slide(self, slide):
        # assert all(slide.left_id != s.left_id and slide.right_id != s.right_id
        #             for s in self.slides)
        
        if self.slides:
            self.score += compute_interest(self.slides[-1].tags, slide.tags)

        self.slides.append(slide)


def compute_interest(s1, s2):
    inter = s1 & s2
    return min(len(inter), len(s1) - len(inter), len(s2) - len(inter))
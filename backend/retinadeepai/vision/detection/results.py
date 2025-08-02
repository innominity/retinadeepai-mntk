import os
from PIL import Image


class DetectionResult:

    def __init__(
        self, points: list, crop_type: int, crop_score: float, is_obb=False
    ) -> None:
        # Массив с точками в формате [x1,y1,x2,y2,x3,y3,x4,y4]
        self.points = points
        self.crop_type = crop_type
        self.crop_score = crop_score
        self.is_obb = is_obb

    def get_top_left(self):
        return (self.points[0], self.points[1])

    def get_top_right(self):
        return (self.points[2], self.points[3])

    def get_bottom_right(self):
        return (self.points[4], self.points[5])

    def get_bottom_left(self):
        return (self.points[6], self.points[7])

    def get_xyxy(self):
        if not self.is_obb:
            return *self.get_top_left(), *self.get_bottom_right()
        
    def get_by_points(self):
        return [
            [self.points[0], self.points[1]],
            [self.points[2], self.points[3]],
            [self.points[4], self.points[5]],
            [self.points[6], self.points[7]],
        ]

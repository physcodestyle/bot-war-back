from modules.coords import Coords
from modules.map import Map
from modules.bot import Bot
from enum import Enum


class DiagonalDirection(Enum):
    from_left_to_right_from_top_to_bottom = 1
    from_right_to_left_from_top_to_bottom = 2
    from_left_to_right_from_bottom_to_top = 3
    from_right_to_left_from_bottom_to_top = 4


class SuperBot(Bot):
    def __init__(self, map: Map, origin: Coords, name: str = 'SuperBot', is_vertical: bool = True):
        super().__init__(map=map, origin=origin, name=name, is_vertical=is_vertical)
        self.search_mode = True
        self.first_round_mode = False
        self.second_round_mode = False
        self.third_round_mode = False
        self.search_coords = []
        self.search_coords_index = 0
        self.last_shot = Coords(top=0, left=0)
        self.success_shots = []
        self.first_round_coords = []
        self.first_round_coords_index = 0
        self.second_round_coords = []
        self.second_round_coords_index = 0
        self.third_round_coords = []
        self.third_round_coords_index = 0
        self.success_first_round_counter = 0
        self.success_second_round_counter = 0


    def shot(self) -> Coords:
        new_shot = Coords(top=1, left=1)
        if self.search_mode:
            new_shot = self._get_next_search_coords()
        else:
            new_shot = self._get_next_round_coords()
        
        return new_shot


    def give_report(self, shot_result: bool):
        if shot_result:
            self.success_shots.append(self.last_shot)
            if self.search_mode:
                self.search_mode = False
                self.first_round_mode = True
            elif self.first_round_mode:
                self.success_first_round_counter += 1
            elif self.second_round_mode:
                self.success_second_round_counter += 1
    

    def _get_next_search_coords(self) -> Coords:
        first = 1
        step = 4
        if len(self.search_coords) == 0:
            width, height = self.map.get_size().get()
            first_points_list = []
            for top in range(first, height, step):
                first_points_list.append(Coords(top=top, left=1))
            for left in range(first, width, step):
                first_points_list.append(Coords(top=1, left=left))
            for first_point in range(len(first_points_list)):
                self.search_coords += self._get_diagonal_coords_list(first_point=first_point)

        new_shot = self.search_coords[self.search_coords_index]
        self.last_shot = new_shot
        self.search_coords_index += 1
        return new_shot


    def _get_next_round_coords(self) -> Coords:
        new_shot = Coords(top=1, left=1)
        if self.first_round_mode:
            if len(self.first_round_coords) == 0:
                self.first_round_coords = self._get_first_round_coords(origin=self.last_shot)
            if self.first_round_coords_index < len(self.first_round_coords):
                new_shot = self.first_round_coords[self.first_round_coords_index]
                self.first_round_coords_index += 1
            else:
                if self.success_first_round_counter == 1:
                    self.first_round_mode = False
                    self.second_round_mode = True
                    self.second_round_coords = self._get_second_round_coords()
                    new_shot = self.second_round_coords[self.second_round_coords_index]
                    self.second_round_coords_index += 1
                elif self.success_first_round_counter == 2:
                    self.first_round_mode = False
                    self.third_round_mode = True
                    self.third_round_coords = self._get_third_round_coords()
                    new_shot = self.third_round_coords[self.third_round_coords_index]
                    self.third_round_coords_index += 1
        elif self.second_round_mode and self.success_second_round_counter > 0:
            new_shot = self.third_round_coords[self.third_round_coords_index]
            self.third_round_coords_index += 1
            self.second_round_mode = False
            self.third_round_mode = True
            self.third_round_coords = self._get_third_round_coords()
        elif self.third_round_mode and self.third_round_coords_index < len(self.third_round_coords):
            new_shot = self.third_round_coords[self.third_round_coords_index]
            self.third_round_coords_index += 1
        
        return new_shot


    def _get_first_round_coords(self, origin: Coords) -> list[Coords]:
        output_list = []
        top, left = origin.get()
        width, height = self.map.get_size().get()

        if top == 1 and left == 1:
            output_list.append(Coords(top=2, left=2))
        elif top == height and left == 1:
            output_list.append(Coords(top=height - 1, left=2))
        elif top == height and left == width:
            output_list.append(Coords(top=height - 1, left=width - 1))
        elif top == 1 and left == width:
            output_list.append(Coords(top=2, left=width - 1))
        else:
            output_list.append(Coords(top=top - 1, left=left - 1))
            output_list.append(Coords(top=top - 1, left=left + 1))
            output_list.append(Coords(top=top + 1, left=left + 1))
            output_list.append(Coords(top=top + 1, left=left - 1))
        
        return output_list


    def _get_second_round_coords(self) -> list[Coords]:
        top0, left0 = self.success_shots[0]
        top1, left1 = self.success_shots[1]
        if (top0 - top1) * (left0 - left1) > 0:
            return [
                Coords(top=top1 - 1, left=left1 + 1),
                Coords(top=top1 + 1, left=left1 - 1),
            ]
        else:
            return [
                Coords(top=top1 - 1, left=left1 - 1),
                Coords(top=top1 + 1, left=left1 + 1),
            ]


    def _get_third_round_coords(self) -> list[Coords]:
        is_vertical = True
        main_line = -1
        width, height = self.map.get_size().get()
        min_top, max_top = height, 0
        min_left, max_left = width, 0
        for shot in self.success_shots:
            top, left = shot.get()
            if top > max_top:
                max_top = top
            if top < min_top:
                min_top = top
            if left > max_left:
                max_left = left
            if left < min_left:
                min_left = left
        if max_left - min_left == 2:
            is_vertical = False
        if is_vertical:
            for shot in self.success_shots:
                top, left = shot.get()
                if top == min_top and left == min_left:
                    main_line = 0
                if top == min_top and left == max_left:
                    main_line = 1
            if main_line == 0:
                return [
                    Coords(top=min_top + 1, left=min_left),
                    Coords(top=min_top, left=max_left),
                    Coords(top=max_top, left=max_left),
                ]
            elif main_line == 1:
                return [
                    Coords(top=min_top + 1, left=max_left),
                    Coords(top=min_top, left=min_left),
                    Coords(top=max_top, left=min_left),
                ]
        else:
            for shot in self.success_shots:
                top, left = shot.get()
                if top == min_top and left == min_left:
                    main_line = 0
                if top == max_top and left == min_left:
                    main_line = 1
            if main_line == 0:
                return [
                    Coords(top=min_top, left=min_left + 1),
                    Coords(top=max_top, left=min_left),
                    Coords(top=max_top, left=max_left),
                ]
            elif main_line == 1:
                return [
                    Coords(top=max_top, left=min_left + 1),
                    Coords(top=min_top, left=min_left),
                    Coords(top=min_top, left=max_left),
                ]


    def _get_diagonal_coords_list(self, first_point: Coords, direction: DiagonalDirection = DiagonalDirection.from_left_to_right_from_top_to_bottom) -> list[Coords]:
        width, height = self.map.get_size().get()
        top, left = first_point.get()
        
        if top > height or top < 1 or left > width or left < 1:
            return []

        output_list = [ first_point ]
        top_increment_sign = 1
        left_increment_sign = 1
        if direction == DiagonalDirection.from_left_to_right_from_bottom_to_top:
            top_increment_sign = -1
        elif direction == DiagonalDirection.from_right_to_left_from_bottom_to_top:
            top_increment_sign = -1
            left_increment_sign = -1
        elif direction == DiagonalDirection.from_right_to_left_from_top_to_bottom:
            left_increment_sign = -1

        while top <= height and top > 0 and left <= width and left > 0:
            top += top_increment_sign
            left += left_increment_sign
            output_list.append(Coords(top=top, left=left))
        
        return output_list
